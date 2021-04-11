import time
import pygame.midi
import uinput
from evdev import UInput, InputDevice
from evdev import UInput, AbsInfo, ecodes as e

pygame.midi.init()

MIDI_DEVICE = "MPK Mini"


def get_midi_device():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, is_input, is_output, opened) = r

        if MIDI_DEVICE in str(name) and is_input:
            return i


MIDI_NOTE_ON = 144
MIDI_NOTE_OFF = 128
MIDI_CONTROL_CHANGE = 176

COARSE_KNOB = 1
FINE_KNOB = 2
COARSE_MOVEMENT = 50
FINE_MOVEMENT = 5

LOWEST_KEY = 48
HIGHEST_KEY = 72

cap = {
    e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT],
    e.EV_REL: [e.REL_X, e.REL_Y],
}


device_id = get_midi_device()
midi_in = pygame.midi.Input(device_id)


device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT])

#ui = UInput(cap, name="example-device", version=0x3)

def hit_ball(velocity):
    FULL_BEANS = -1000

    power = int(FULL_BEANS * (velocity / 128))

    # Click mouse down
    print("clicking down")
    device.emit(uinput.BTN_LEFT, 1)
    time.sleep(0.1)

    # Move mouse up to match velocity
    print(f"setting velocity to {power}")
    device.emit(uinput.REL_Y, power)
    time.sleep(0.1)

    # Mouse up
    print("clicking up")
    device.emit(uinput.BTN_LEFT, 0)

coarse_last_pos = 0
fine_last_pos = 0
while True:
    if midi_in.poll():
        midi_events = midi_in.read(999)
        print(midi_events)
        for midi_event in midi_events:
            status_code, data_0, data_1, _ = midi_event[0]
            if status_code == MIDI_CONTROL_CHANGE:
                dial_num = data_0
                dial_pos = data_1

                if dial_num == COARSE_KNOB:
                    delta = dial_pos - coarse_last_pos
                    coarse_last_pos = dial_pos
                    movement = COARSE_MOVEMENT
                elif dial_num == FINE_KNOB:
                    delta = dial_pos - fine_last_pos
                    fine_last_pos = dial_pos
                    movement = FINE_MOVEMENT

                device.emit(uinput.REL_X, delta * movement)

            elif status_code == MIDI_NOTE_ON:
                velocity = data_1
                key = data_0
                velocity = (key - LOWEST_KEY) / (HIGHEST_KEY - LOWEST_KEY) * 128
                hit_ball(velocity)


