# Last.fm Syncing Tool
# Based on https://github.com/huberf/lastfm-scrobbler
# Last.fm API: https://www.last.fm/api

import time
import requests
import hashlib

api_head = 'http://ws.audioscrobbler.com/2.0/'

def authorize(auth):
    params = {
            'api_key': auth['api'],
            'method': 'auth.getSession',
            'token': auth['user_token']
            }
    requestHash = hashRequest(params, auth['secret'])
    params['api_sig'] = requestHash
    apiResp = requests.post(api_head, params)
    return apiResp.text

def nowPlaying(auth, song_name, artist_name, album_name):
    params = {
            'method': 'track.updateNowPlaying',
            'api_key': auth['api'],
            'track': song_name,
            'artist': artist_name,
            'album': album_name,
            'sk': auth['session_key']
            }
    requestHash = hashRequest(params, auth['secret'])
    params['api_sig'] = requestHash
    apiResp = requests.post(api_head, params)
    return apiResp.text

def scrobble(auth, song_name, artist_name, album_name):
    # Currently this sort of cheats the timestamp protocol
    params = {
            'method': 'track.scrobble',
            'api_key': auth['api'],
            'timestamp': str( int(time.time() - 30) ),
            'track': song_name,
            'artist': artist_name,
            'album': album_name,
            'sk': auth['session_key']
            }
    requestHash = hashRequest(params, auth['secret'])
    params['api_sig'] = requestHash
    apiResp = requests.post(api_head, params)
    return apiResp.text

def hashRequest(obj, secretKey):
    string = ''
    items = obj.keys()
    items = sorted(items)
    for i in items:
        string += i
        string += obj[i]
    string += secretKey
    stringToHash = string.encode('utf8')
    requestHash = hashlib.md5(stringToHash).hexdigest()
    return requestHash
