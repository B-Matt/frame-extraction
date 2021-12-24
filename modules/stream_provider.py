import os

class StreamProvider(object):
    def __init__(self, path, ext) -> None:
        self._media_files = []
        self._path = path
        self._file_ext = ext
        self._index = 0

    def open(self):
        for file in os.listdir(self._path):
            if os.path.splitext(file)[1] == f'.{self._file_ext}':
                self._media_files.append(os.path.join(self._path, file))
        self._media_files.sort()

        print('[PLAYLIST]:')
        for i, file in enumerate(self._media_files):
            print(f'[{i}] {file}')

    def data(self):
        if self._index == len(self._media_files):
            return b''

        with open(self._media_files[self._index], 'rb') as stream:
            data = stream.read()

        self._index = self._index + 1
        return data
