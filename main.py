import vlc
import keyboard
import time
import math
from multiprocessing import Pool
from tqdm import tqdm

from modules.stream_provider import *
from modules.player_utils import *
from modules.compressor import *
from modules.file_sorter import *
from modules.duplicates import *

if __name__ == '__main__':
    instance = vlc.Instance('--rate=3.0')
    sorter = FileSorter('data', 'screenshots')
    duplicate_remover = DuplicatesRemover('screenshots')

    player = instance.media_player_new()
    provider = StreamProvider('videos', 'mp4', instance, 'screenshots')
    player.set_media(provider.open())

    player_utils = VLCPlayerUtils(player)
    player.play()

    while True:
        if keyboard.is_pressed('q'):
            player.pause()
            time.sleep(0.08)

            current_frame = player.get_time() / player_utils.mspf()
            frame_count = math.ceil(player.get_fps())
            for i in range(frame_count * 2):
                player_utils.frame_backward()
                time.sleep(0.5)
                player.video_take_snapshot(0, f'screenshots/{provider.get_name()}', 1920, 1080)

            player.set_time(math.ceil(current_frame * player_utils.mspf()))
            time.sleep(0.3)

            for i in range(frame_count * 2):
                player_utils.frame_forward()
                time.sleep(0.5)
                player.video_take_snapshot(0, f'screenshots/{provider.get_name()}', 1920, 1080)


            player.set_time(math.ceil(current_frame * player_utils.mspf()))
            time.sleep(0.3)
            player.play()
            continue

        if keyboard.is_pressed('right'):
            player_utils.sec_forward(0.5)

        if keyboard.is_pressed('left'):
            player_utils.sec_backward(0.5)

        if keyboard.is_pressed('f4'):
            duplicate_remover.detect_same_images()
            break

    player.stop()

    # Remove Duplicated Images
    pool = Pool(processes=duplicate_remover._process_num)
    pool.map(duplicate_remover.detect_same_images, duplicate_remover._chunked_paths)
    pool.close()
    pool.join()

    # Sort & Compress Images To WebP Format
    sorter.move_files()
    #compressor = Compressor('screenshots', 100, 6)