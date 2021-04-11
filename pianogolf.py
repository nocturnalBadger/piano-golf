import time
import pygame.midi
import sys

if sys.platform == "linux":
    from linuxmouse import mouse
elif sys.platform == "win32":
    from windowsmouse import mouse


# Name or prefix for the midi input device to use
MIDI_DEVICE = "MPK Mini"

# Midi status codes for key functions
# https://www.midi.org/specifications-old/item/table-2-expanded-messages-list-status-bytes
MIDI_NOTE_ON = 144
MIDI_NOTE_OFF = 128
MIDI_CONTROL_CHANGE = 176

# Definitions for side-to-side controls
MOVEMENT_KNOBS = {
    1: 50, # Midi control #1 moves 50 mouse units per unit, etc.
    2: 5,
    3: 1
}

# Set the midi knob to control spin (if enabled in game)
SPIN_KNOB = 5

# Definitions for key range (my AKAI MPK mini goes from c3 to c5)
# This makes middle c exactly half power
LOWEST_KEY = 48
HIGHEST_KEY = 72

# Use midi velocity to determine hit speed. Interesting but very touchy.
VELOCITY_MODE = False

setting_spin = False
spin_adj_time = time.time()


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
    FULL_BEANS = -500

    power = int(FULL_BEANS * (velocity / 128))

    # Click mouse down
    print("clicking down")
    mouse.click_down()
    time.sleep(0.1)

    # Move mouse up to match velocity
    print(f"setting velocity to {power}")
    mouse.move_y(power)
    time.sleep(0.1)

    # Mouse up
    print("clicking up")
    mouse.click_up()

def set_spin(spin_value):
    FULL_SPIN = 350
    print(f"setting spin to {spin_value}")

    spin_value = int(-FULL_SPIN * ((spin_value - 128 / 2) / 128))
    print(f"moving mouse {spin_value} units to achieve spin")

    mouse.right_click_down()

    mouse.move_x(spin_value)

    mouse.right_click_up()


def handle_event(status_code, data_0, data_1, control_state):
    """ Handle a midi event """
    if status_code == MIDI_CONTROL_CHANGE:
        dial_num = data_0
        dial_pos = data_1

        # Compare position with known control state
        last_pos = control_state[dial_num]
        delta = dial_pos - last_pos

        if dial_num in MOVEMENT_KNOBS:
            movement = MOVEMENT_KNOBS[dial_num]
            mouse.move_x(delta * movement)

        if dial_num == SPIN_KNOB:
            set_spin(dial_pos)

        control_state[dial_num] = dial_pos


    elif status_code == MIDI_NOTE_ON:
        key = data_0
        if VELOCITY_MODE:
            velocity = data_1
        else:
            velocity = (key - LOWEST_KEY) / (HIGHEST_KEY - LOWEST_KEY) * 128
        hit_ball(velocity)

    elif status_code == 129:
        mouse.click_down()

    return control_state

def loop():
    """ Main event loop """
    # Record knob positions
    control_state = {x: 0 for x in range(1, 9)}
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

    try:
        loop()
    except KeyboardInterrupt:
        pass
