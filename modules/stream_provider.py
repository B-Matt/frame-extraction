import os
import vlc

class StreamProvider(object):
    def __init__(self, path, ext, vlc_instance) -> None:
        self._media_files = []
        self._path = path
        self._file_ext = ext
        self._index = 0
        self._instance = vlc_instance

        self.setup()

    def setup(self):
        for file in os.listdir(self._path):
            if os.path.splitext(file)[1] == f'.{self._file_ext}':
                self._media_files.append(os.path.join(self._path, file))
        self._media_files.sort()

        print('[PLAYLIST]:')
        for i, file in enumerate(self._media_files):
            print(f'[{i}] {file}')

    def open(self):
        if self._index == len(self._media_files):
            return b''

        data = self._instance.media_new(self._media_files[self._index])
        self._index = self._index + 1
        return data
