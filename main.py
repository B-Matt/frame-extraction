import vlc
import keyboard
import time
import math

from modules.stream_provider import *

def mspf(mp):
    """Milliseconds per frame"""
    return int(1000 // (mp.get_fps() or 25))

instance = vlc.Instance()
provider = StreamProvider('videos', 'mp4', instance)

player = instance.media_player_new()
  
player.set_media(provider.open())
player.play()

while True:
    try:
        if keyboard.is_pressed('q'):
            #print(player.get_position())
            time.sleep(0.08)
            player.pause()
            time.sleep(0.08)

            current_frame = player.get_time() / mspf(player)
            for i in range(math.ceil(player.get_fps())):
                print(i, math.ceil((current_frame - i) * mspf(player)))
                player.set_time(math.ceil((current_frame - i) * mspf(player)))
                time.sleep(0.25)
                player.video_take_snapshot(0, 'screenshots', 1920, 1080)

            #player.set_time(13401)
            #player.set_position(0.013967541977763176)
            time.sleep(0.1)
            #player.video_take_snapshot(0, 'screenshots', 0, 0)
            break
    except:
        break

player.stop()