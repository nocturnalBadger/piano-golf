import threading
import fluidsynth
import time

class Player:

    def __init__(self):
        self.fs = fluidsynth.Synth()
        self.fs.start()

        sfid = self.fs.sfload("FORE.sf2")
        self.fs.program_select(0, sfid, 0, 0)

    def start_note(self, key, velocity):
        self.fs.noteon(0, key, velocity)

    def end_note(self, key):
        self.fs.noteoff(0, key)

    def play_note(self, key, velocity):
        self.start_note(key, velocity)

        timer = threading.Timer(1, self.end_note, [key])
        timer.start()

player = Player()
