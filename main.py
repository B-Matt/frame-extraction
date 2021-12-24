import vlc
import ctypes

from modules.stream_provider import *
from modules.callbacks import *

provider = StreamProvider('videos', 'mp4')
provider_obj = ctypes.py_object(provider)
provider_ptr = ctypes.byref(provider_obj)

instance = vlc.Instance()
media = instance.media_new_callbacks(callback_media_open, callback_media_read, media_seek_cb, media_close_cb, provider_ptr)
player = media.player_new_from_media()

player.play()
input("press enter to quit")
player.stop()