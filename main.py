import vlc
import keyboard
import time

from modules.stream_provider import *
from modules.callbacks import *

instance = vlc.Instance()
provider = StreamProvider('videos', 'mp4', instance)

player = instance.media_player_new()
  
player.set_media(provider.open())
player.play()

while True:
    try:
        if keyboard.is_pressed('q'):
            #print(player.get_position())
            print(player.get_fps())
            player.set_position(0.013967541977763176)
            time.sleep(0.08)
            player.pause()

            player.video_take_snapshot(0, 'screenshots', 0, 0)
            break
    except:
        break

player.stop()