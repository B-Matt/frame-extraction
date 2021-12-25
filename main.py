import vlc
import keyboard
import time
import math

from modules.stream_provider import *
from modules.frame_capture import *

instance = vlc.Instance('')
player = instance.media_player_new()
provider = StreamProvider('videos', 'mp4', instance, 'screenshots')
player.set_media(provider.open())

capturer = FrameCapture(player)
player.play()

while True:
    if keyboard.is_pressed('q'):
        time.sleep(0.08)
        player.pause()
        time.sleep(0.08)

        current_frame = player.get_time() / capturer.mspf()
        frame_count = math.ceil(player.get_fps())
        for i in range(frame_count * 2):
            capturer.frame_backward()
            time.sleep(0.5)
            player.video_take_snapshot(0, f'screenshots/{provider.get_name()}/backward', 1920, 1080)
            time.sleep(0.2)

        player.set_time(math.ceil(current_frame * capturer.mspf()))
        time.sleep(0.3)

        for i in range(frame_count * 2):
            capturer.frame_forward()
            time.sleep(0.5)
            player.video_take_snapshot(0, f'screenshots/{provider.get_name()}/forward', 1920, 1080)
            time.sleep(0.2)

        player.set_time(math.ceil(current_frame * capturer.mspf()))

        time.sleep(0.3)
        player.play()
        continue

    if keyboard.is_pressed('enter'):
        break

player.stop()