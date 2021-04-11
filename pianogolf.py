import time
import pygame.midi
import uinput
from dataclasses import dataclass


# Name or prefix for the midi input device to use
MIDI_DEVICE = "MPK Mini"

# Midi status codes for key functions
# https://www.midi.org/specifications-old/item/table-2-expanded-messages-list-status-bytes
MIDI_NOTE_ON = 144
MIDI_NOTE_OFF = 128
MIDI_CONTROL_CHANGE = 176

# Definitions for side-to-side controls
COARSE_KNOB = 1
FINE_KNOB = 2
COARSE_MOVEMENT = 50
FINE_MOVEMENT = 5

# Definitions for key range (my AKAI MPK mini goes from c3 to c5)
# This makes middle c exactly half power
LOWEST_KEY = 48
HIGHEST_KEY = 72

# Use midi velocity to determine hit speed. Interesting but very touchy.
VELOCITY_MODE = False


def get_midi_device():
    """
    Search for a midi device with the substring set in MIDI_DEVICE 
    return the device id (int)
    """
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, is_input, is_output, opened) = r

        if MIDI_DEVICE in str(name) and is_input:
            return i
    raise ValueError("Midi device not found")

def hit_ball(velocity):
    """
    Script mouse movements to make a shot with the given velocity
    :param velocity: relative shot power from 0 to 128
    """
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

def handle_event(status_code, data_0, data_1, control_state):
    """ Handle a midi event """
    coarse_last_pos, fine_last_pos = control_state
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
        key = data_0
        if velocity_mode:
            velocity = data_1
        else:
            velocity = (key - LOWEST_KEY) / (HIGHEST_KEY - LOWEST_KEY) * 128
        hit_ball(velocity)

    return (coarse_last_pos, fine_last_pos)

def loop():
    """ Main event loop """
    # Record knob positions
    control_state = (0, 0)
    while True:
        if midi_in.poll():
            midi_events = midi_in.read(999)
            print(midi_events)
            for midi_event in midi_events:
                status_code, data_0, data_1, _ = midi_event[0]
                control_state = handle_event(status_code, data_0, data_1, control_state)


if __name__ == "__main__":
    pygame.midi.init()
    device_id = get_midi_device()
    midi_in = pygame.midi.Input(device_id)

    device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT])

    try:
        loop()
    except KeyboardInterrupt:
        pass
