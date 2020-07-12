import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import pprint
import requests
import vlc
import pafy
import time
from itertools import cycle

# list of the video ids used in the cycle between the ads
list_of_sess = cycle(['qVdPh2cBTN0', 'L3wKzyIN1yk', 'LHCob76kigA', 'mtf7hC17IBM', 'MYSVMgRr6pw', 'uXeZNXdu-gs', '8UVNT4wvIGY', 'MsTWpbR_TVE', '0-7IHOXkiV8', '1Al-nuR1iAU'] )

def play_yt():
    global list_of_sess
    Instance = vlc.Instance('--no-video')
    player = Instance.media_player_new()
    try:
        url = 'https://www.youtube.com/watch?v=' + next(list_of_sess)
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        # print(playurl)
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        # pprint.pprint(dir(player) )
        
        # print(player.is_playing())
        player.play()
        time.sleep(5)
    except :
        print("Issue with the song or the video id")
        
        
    while True: # player is non blocking and
        if player.is_playing() == 0:
            break


def check_for_ad_playing(track):
    return track['currently_playing_type']=='ad'

def check_for_spotify_ads(token, spotifyObject):
    devices = spotifyObject.devices()
    deviceID = devices['devices'][0]['id']

    # Current track information
    track = spotifyObject.current_user_playing_track()
    pprint.pprint(track)
    import subprocess
    while True:
        if check_for_ad_playing(track):
            subprocess.call([ 'osascript' ,'-e' ,"tell application \"Spotify\" to set sound volume to 0"])
            play_yt()
            subprocess.call([ 'osascript', '-e', 'tell application "Spotify" to set player position to 0'])
            subprocess.call([ 'osascript' ,'-e' ,"tell application \"Spotify\" to set sound volume to 100"])
        time.sleep(40)
    
# check_for_spotify_ads()
username = os.getenv('SPOTIFY_USERNAME')
scope = 'user-read-private user-read-playback-state user-modify-playback-state'


scope = 'user-read-private user-read-playback-state user-modify-playback-state'
try:
    token = util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope) # add scope

spotifyObject = spotipy.Spotify(auth=token)
print(token)

check_for_spotify_ads(token, spotifyObject)

