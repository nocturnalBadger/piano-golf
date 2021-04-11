# Piano Golf

Midi control mapper for Golf With your Friends

Have you ever wanted to play golf with a piano? No? Oh well. 

This project reads inputs from a midi controller (I'm using an AKAI MPK Mini) and translates it into mouse movements to make a shot in the game Golf With Your Friends.

## Features
* Set your trajectory with K1-K3 ( in order of coarse to fine control). 
* Fire using any of the note keys. The lowest note (c3) for minimum power; highest note (c5) for maximum power.
* Optionally, use midi velocity input to set stroke power (cool idea but very touchy)
* Tap Pad 5 to hold left click (enables the aiming reticle)
* [experimental] Use K5 to set spin on the ball (if enabled in game)

## Requirements
* pygame
* [pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth)
* [fluidsynth](https://github.com/FluidSynth/fluidsynth/releases)

Uses uinput on Linux to simulate mouse movements; ctypes on Windows.

## Usage
```
python pianogolf.py
```
