import os
import shutil
from enum import Enum

class PlayerState(Enum):
    PLAYING = 1
    STOPPED = 2
    PAUSED = 3

class StreamProvider(object):
    def __init__(self, path, ext, vlc_instance, player, screens_path) -> None:
        self.current_state = PlayerState.STOPPED

        self._media_files = []
        self._files_names = []

        self._path = path
        self._file_ext = ext
        self._index = 0
        self._instance = vlc_instance
        self._player = player
        self._screens_path = screens_path
        self.setup()

    def setup(self):
        for file in os.listdir(self._path):
            if os.path.splitext(file)[1] == f'.{self._file_ext}':
                self._media_files.append(os.path.join(self._path, file))
                self._files_names.append(os.path.splitext(file)[0])
        self._media_files.sort()

        print('[PLAYLIST]:')
        for i, file in enumerate(self._media_files):
            print(f'[{i}] {file}')

    def open(self):
        if self._index == len(self._media_files):
            return b''
        data = self._instance.media_new(self._media_files[self._index])

        # Create New Directory In Screenshots
        path = os.path.join(self._screens_path, self._files_names[self._index])
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)        
        os.mkdir(path)  # Video Directory

        # Increament Index
        self._index = self._index + 1
        return data

    def play(self):
        if self.current_state == PlayerState.STOPPED:
            self._player.play()
            self.current_state = PlayerState.PLAYING

    def pause(self):
        if self.current_state == PlayerState.PAUSED:
            self._player.play()
            self.current_state = PlayerState.PLAYING
        elif self.current_state == PlayerState.PLAYING:
            self._player.pause()
            self.current_state = PlayerState.PAUSED

    def get_name(self):
        return self._files_names[self._index - 1]
