#!/usr/bin/env python
"""Every ten minutes-ish, take a webcam picture and screenshot.

This script is based on gwern's `sousveillance.sh` script, posted to
the LessWrong forum at
<http://lesswrong.com/lw/2qv/antiakrasia_remote_monitoring_experiment/2s3n>.

Usage
-----

Put this script somewhere convenient (ex: `~/scripts/sousveillance.py`) and
add an entry to your crontab:

    0,10,20,30,40,50 * * * * ~/scripts/sousveillance.py

Motivation
----------

Stay focused, and keep track of the fact. Also, pictures!

Required Tools (OSX)
--------------------

`imagesnap` - <http://iharder.sourceforge.net/current/macosx/imagesnap/>
`screencapture` - /usr/sbin/screencapture

Notes
-----

Original post (and script):
------------------------------------------------------------------------------
  In the spirit of my memento-mori.sh, I've written a script to sleep
  randomly 0-10 minutes and take a screenshot & webcam shot. Obviously many
  of the values are specific to my own computer (such as the names in /proc,
  where in ~/ the pictures are sent to, and the use of ImageMagick,
  jpegoptim, and OptiPNG), but it should be easy to adapt to your own
  computer:

    #!/bin/sh
    set -e
    if grep open /proc/acpi/button/lid/LID?/state > /dev/null
    then
    CURRENT=`date +%s`;
    SLEEP=$(( $CURRENT % 10 ))
    TIMEOUT="m"
    sleep $SLEEP$TIMEOUT
    import -quality 100 -window root png:$HOME/photos/webcam/xwd-$CURRENT.png
    fswebcam --resolution 1280x1024 -S 2 -F 3 ~/photos/webcam/$CURRENT.jpg
    optipng -o9 -fix `ls -t ~/photos/webcam/*.png | head -1`
    jpegoptim -m50 `ls -t ~/photos/webcam/*.jpg | head -1`
    fi

  This would be called from one's crontab like so:

    0,10,20,30,40,50 * * * * ~/bin/bin/sousveillance.sh

  My original script ran every hour on the hour, but I discovered that this
  was so predictable that I was beginning to work-around it by switching to
  a more kosher good-looking application, and wasn't frequent enough anyway.
  Hopefully the randomized version will work better.
------------------------------------------------------------------------------
"""

from os.path import join, exists, expanduser
from os import makedirs
import random
import time
import subprocess
from datetime import datetime

def ensure_path(*paths):
  for path in paths:
    if not exists(path):
      makedirs(path)

def touch(fname):
    with open(fname, 'a'):
        os.utime(fname)


HOME_DIR = expanduser('~')

imagesnap = join(HOME_DIR, 'bin/imagesnap')
screencapture = "/usr/sbin/screencapture"

SNAPSHOT_DIR = join(HOME_DIR, 'archive', 'sousveillance', 'snapshots')
SCREENSHOT_DIR = join(HOME_DIR, 'archive', 'sousveillance', 'screenshots')
ensure_path(SNAPSHOT_DIR, SCREENSHOT_DIR)

# Sleep between 0 seconds and 9 minutes, 59 seconds
rand_sleep_seconds = random.randint(0, 10*60-1)
time.sleep(rand_sleep_seconds)

# Filename corresponds to current time (in UTC, i.e. timezone agnostic)
filename = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
snapshot_dst = join(SNAPSHOT_DIR,  filename)
screenshot_dst = join(SCREENSHOT_DIR,  filename)

# Take a picture!
subprocess.check_output([
    imagesnap,
    "-w", "1.00", # allow one second for iSight warmup and ISO adjustment
    snapshot_dst
])

# Take a screenshot!
subprocess.check_output([
    screencapture,
    "-Cox",     # [C]ursor included, [o]mit shadow, i[x]nay the ellbay
    "-tjpg",    # [jpg] format
    "-T0",      # [0] second delay
    screenshot_dst
])
