import vlc

class FrameCapture(object):
    def __init__(self, player) -> None:
        self._player = player

    def mspf(self):
        return int(1000 // (self._player.get_fps() or 25))

    def frame_forward(self):
        self._player.set_time(self._player.get_time() + self.mspf())

    def frame_backward(self):
        self._player.set_time(self._player.get_time() - self.mspf())