#!/usr/bin/env python
import sys
import os
import logging, logging.handlers
import subprocess

LOG_FILE='/home/pi/.flexget/torrent_complete.log'
XBMC_HOST='127.0.0.1'

log = logging.getLogger("torrent_complete")
log.setLevel(logging.DEBUG)
logformat = logging.Formatter("%(levelname)s\t%(asctime)s\t%(message)s")

logfile = logging.FileHandler(LOG_FILE)
logfile.setFormatter(logformat)
#logfile.setLevel(logging.INFO)
log.addHandler(logfile)

if len(sys.argv) != 4:
	log.error('%s called with %d arguments, it requires 3.' % (sys.argv[0],(len(sys.argv)-1)))
	log.info('Usage: '+sys.argv[0]+' <torrent_id> <torrent_name> <torrent_path>')
	log.info('This script was made to be called from the Execute plugin in deluge. Please')
	log.info('see http://dev.deluge-torrent.org/wiki/Plugins/Execute for more information')
	sys.exit(-1)


torrent_id=sys.argv[1]
torrent_name=sys.argv[2]
torrent_path=(sys.argv[3] if (sys.argv[3][-1] == '/') else sys.argv[3]+'/')

log.debug("%s called with torrent_id='%s', torrent_name='%s', torrent_path='%s'." % (sys.argv[0],torrent_id, torrent_name, torrent_path))

file_name = torrent_path + torrent_name

log.debug("Checking if it is a file or directory")

if not os.path.isfile(file_name):
	log.debug("Is not a file")

	if os.path.exists(file_name):
		log.debug("Is a directory")
		for f in os.listdir(file_name):
			if f.endswith(".mp4") or f.endswith(".avi") or f.endswith(".mkv"):
				log.debug(f)
				log.debug(os.path.join(file_name,f))

log.debug("Updating XBMC Library")
ret = subprocess.call('/home/pi/.flexget/kodi-send.py --action="XBMC.updatelibrary(video,' + torrent_path + ' )"', shell=True)

log.debug(ret)

#if ret != 0:
	#log.warning('Update XBMC command returned non-zero value %d.' % ret)

log.debug(" ")

sys.exit(0)
