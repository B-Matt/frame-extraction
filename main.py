import vlc
import keyboard
import time
import math

from modules.stream_provider import *
from modules.player_utils import *
from modules.compressor import *
from modules.file_sorter import *

instance = vlc.Instance('--rate=5.0')
sorter = FileSorter('data', 'screenshots')

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
            player.video_take_snapshot(0, f'screenshots/{provider.get_name()}/backward', 1920, 1080)

        player.set_time(math.ceil(current_frame * player_utils.mspf()))
        time.sleep(0.3)

        for i in range(frame_count * 2):
            player_utils.frame_forward()
            time.sleep(0.5)
            player.video_take_snapshot(0, f'screenshots/{provider.get_name()}/forward', 1920, 1080)


        player.set_time(math.ceil(current_frame * player_utils.mspf()))
        time.sleep(0.3)
        player.play()
        continue

    if keyboard.is_pressed('right'):
        player_utils.sec_forward(0.5)

    if keyboard.is_pressed('left'):
        player_utils.sec_backward(0.5)

    if keyboard.is_pressed('space'):
        break

player.stop()
sorter.move_files()
#compressor = Compressor('screenshots', 100, 6)