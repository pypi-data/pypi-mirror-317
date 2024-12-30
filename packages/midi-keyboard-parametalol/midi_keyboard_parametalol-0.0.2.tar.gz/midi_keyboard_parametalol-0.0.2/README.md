# MIDI to Keyboard event mapper

The hardcoded mapping translates the Soft and Sostenuto pedal pushes to Page Up and Page Down events accordingly.

## Requirements

* Python3
* python-rtmidi
* evdev

## Usage

```console
sh$ midi-keyboard
Do you want to create a virtual MIDI input port? (y/N) N
Available MIDI ports:

[0] Midi Through:Midi Through Port-0 14:0
[1] Clavinova:Clavinova MIDI 1 32:0

Select MIDI input port (Control-C to exit): 1
^C⏎
```
