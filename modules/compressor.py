import os
from tqdm import tqdm

from PIL import Image

class Compressor(object):
    def __init__(self, path, quality, method):
        self._path = path
        self._quality = quality
        self._method = method
        
        image_list = self.list_image_files()
        self.convert_image_batch(image_list)

    def convert(self, img_path):
        save_path = img_path.split('.')[0]
        image = Image.open(img_path)
        image = image.convert('RGB')
        image.save(fp=f'{save_path}.webp', format='webp', lossless=True, quality=self._quality, method=self._method)

    def list_image_files(self):
        files_list = list()
        for (dirpath, dirnames, filenames) in os.walk(self._path):
            files_list += [os.path.join(dirpath, file) for file in filenames]
        return files_list

    def convert_image_batch(self, image_list):
        print('\n\n[CONVERTING BATCH OF IMAGES INTO WEBP FORMAT]:')
        for path in tqdm(image_list):
            self.convert(path)
            os.unlink(path)
