import os
import uuid
import shutil

class FileSorter(object):
    """
        Class used for moving all screenshots from the screenshots directory to the data directory.
        Every file that is being moved will get a new unique name generated with the UUID v4 generator.
    """
    def __init__(self, save_path, data_path):
        self._save_path = save_path
        self._data_path = data_path

        if not os.path.isdir(self._save_path):
            os.mkdir(self._save_path)

    def list_files(self):
        files_list = list()
        for (dirpath, dirnames, filenames) in os.walk(self._data_path):
            files_list += [os.path.join(dirpath, file) for file in filenames]
        return files_list    
    
    def move_files(self):
        files_to_move = self.list_files()
        for file_path in files_to_move:
            shutil.move(file_path, f"{self._save_path}/{str(uuid.uuid4())}.png")

