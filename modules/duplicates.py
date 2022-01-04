import os
import cv2
import numpy as np

from multiprocessing import cpu_count

from .utils import list_files, chunk

class DuplicatesRemover(object):
    def __init__(self, data_path):
        self._data_path = data_path        
        self._all_images = list_files(self._data_path)

        self._process_num = cpu_count() + 1
        self._process_ids = list(range(0, self._process_num))
        #self._images_per_process = len(self._all_images) / float(self._process_num)
        #self._images_per_process = int(np.ceil(self._images_per_process))
        self._images_per_process = 192
        self._chunked_paths = list(chunk(self._all_images, self._images_per_process))

    def detect_same_images(self, data):
        FLANN_INDEX_LSH = 6
        index_params= dict(algorithm = FLANN_INDEX_LSH,
                        table_number = 12, # 12
                        key_size = 20,     # 20
                        multi_probe_level = 2) #2

        search_params = dict(checks=100)   # or pass empty dictionary
        detector = cv2.ORB_create(nfeatures=10000, scoreType=cv2.ORB_FAST_SCORE)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        for (i, image) in enumerate(data):
            if not os.path.exists(image):
                continue
            first_img = cv2.imread(image, 0)
            kp1, des1 = detector.detectAndCompute(first_img, None)

            for next_image in data[i+1:]:
                if not os.path.exists(next_image):
                    continue

                second_img = cv2.imread(next_image, 0)
                kp2, des2 = detector.detectAndCompute(second_img, None)

                if (des1 is None or len(des1) < 2 or des2 is None or len(des2) < 2):
                    continue

                matches = flann.knnMatch(des1, des2, k=2)
                good_matches = 0

                for t in matches:
                    if len(t) > 1:
                        if t[0].distance < 0.75 * t[1].distance:
                            good_matches += 1

                if good_matches > 900:
                    os.remove(next_image)
