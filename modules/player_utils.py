
class VLCPlayerUtils(object):
    """
        Class used for changing VLC Player frames and seconds forward or backwards.
    """
    def __init__(self, player) -> None:
        self._player = player

    def mspf(self):
        return int(1000 // (self._player.get_fps() or 25))

    def frame_forward(self):
        self._player.set_time(self._player.get_time() + self.mspf())

    def frame_backward(self):
        self._player.set_time(self._player.get_time() - self.mspf())

    def sec_forward(self, secs=1):
        self._player.set_time(self._player.get_time() + secs * 1000)

    def sec_backward(self, secs=1):
        self._player.set_time(self._player.get_time() - secs * 1000)