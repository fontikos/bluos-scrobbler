# BluOS Scrobbler
# BluOS API: https://bluos.net/wp-content/uploads/2020/06/Custom-Integration-API-v1.0.pdf

import requests
import xml.etree.cElementTree as et
import lastfm
import datetime
import time
import myconfig
import re
import sys

auth = {}
auth['api'] = myconfig.LASTFM_API
auth['secret']= myconfig.LASTFM_SECRET
auth['session_key'] = myconfig.LASTFM_SESSION_KEY
auth['user_token'] = ''
BLUOS_STATUS_URL = 'http://%s:%d/Status' % (myconfig.BLUOS_IP, myconfig.BLUOS_PORT)

def handle_response(rsp):
	root = et.fromstring(rsp)
	if root.attrib['status'] != 'ok':
		print(rsp, file=sys.stderr)
	return


song = {}
song['etag'] = ''
song['timeout'] = 300
song['scrobble'] = False
oldnp = 0
while True:
	# requests.exceptions.ConnectionError
	if song['etag'] == '':
		r = requests.get(BLUOS_STATUS_URL)
	else:
		r = requests.get('%s?timeout=%d&etag=%s' % (BLUOS_STATUS_URL, song['timeout'], song['etag']))

	#print(r.text)
	root=et.fromstring(r.text)
	
	try:
		oldetag = song['etag']
		song['etag'] = root.attrib['etag']
		song['service'] = root.find('service').text
		if song['service'] not in myconfig.SCROBBLE_SERVICES:
			continue
		
		song['artist'] = root.find('artist').text
		if ',' in song['artist']:
			song['artist'] = song['artist'].split(',')[0]

		if root.find('name') != None:
			song['title'] = root.find('name').text
		else:
			song['title'] = root.find('title1').text
		song['title'] = re.sub(r'\(.*?Remaster.*?\)','', song['title'])
		song['title'] = song['title'].strip()

		song['album'] = root.find('album').text
		song['album'] = re.sub(r'\(.*?Remaster.*?\)','', song['album'])
		song['album'] = song['album'].strip()

		song['state'] = root.find('state').text
		song['secs'] = int(root.find('secs').text)
	except AttributeError:
		#print(r.text)
		continue

	if song['secs'] <= 1 and (song['state'] in ['play', 'stream']):
		song['timeout'] = myconfig.SCROBBLE_AFTER
		song['scrobble'] = True
		tnow = time.time()
		if tnow - oldnp > 1:
			rsp = lastfm.nowPlaying(auth, song['title'], song['artist'], song['album'])
			oldnp = tnow
			handle_response(rsp)
			print('[%s] New Song!' % str(datetime.datetime.now()))
			print(song)

	if song['scrobble'] and oldetag == song['etag'] and song['secs'] > 20 and song['state'] in ['play', 'stream']:
		song['timeout'] = 300
		song['scrobble'] = False
		rsp = lastfm.scrobble(auth, song['title'], song['artist'], song['album'])
		handle_response(rsp)
		print('[%s] Scrobble!' % str(datetime.datetime.now()))
		print(song)
