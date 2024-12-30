import contextlib
import sys

from evdev import UInput
from evdev import ecodes as e
from rtmidi import midiutil

MIDI_CONTROL = 176
MIDI_VALUE_PUSH = 127
EV_KEY_DOWN = 1
EV_KEY_UP = 0


CONTROL_PEDAL_SOSTENUTO = 67
CONTROL_PEDAL_SOFT = 66


class Mapper:
    def __init__(self, mapping, port_name=None):
        self.ui = UInput()
        self.mapping = mapping
        self.midi, _output = midiutil.open_midiinput(
            port=port_name, use_virtual=False, interactive=True, client_name='midi-keyboard'
        )

    def _key_press(self, key):
        self.ui.write(e.EV_KEY, key, EV_KEY_DOWN)
        self.ui.write(e.EV_KEY, key, EV_KEY_UP)
        self.ui.syn()

    def _midi_event(self, ch, note, velocity):
        if ch == MIDI_CONTROL and velocity == MIDI_VALUE_PUSH and note in self.mapping:
            self._key_press(self.mapping[note])

    def run(self):
        def cbk(msg_delta, self: Mapper):
            self._midi_event(*msg_delta[0])

        self.midi.set_callback(cbk, self)
        input()

    def stop(self):
        self.midi.close_port()
        self.ui.close()


def main() -> int:
    m = Mapper(
        {CONTROL_PEDAL_SOSTENUTO: e.KEY_PAGEUP, CONTROL_PEDAL_SOFT: e.KEY_PAGEDOWN},
    )
    with contextlib.suppress(KeyboardInterrupt):
        m.run()
    m.stop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
