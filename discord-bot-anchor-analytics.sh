#!/bin/sh

# Config
USER=discord
OUTPUT=log.log
ERROR=err.err
SCRIPT=discord-bot-anchor-analytics.py

# Stop process if already running
PROCESS_IDS=$(pidof python3 $SCRIPT)
if [ $PROCESS_IDS ]; then
	kill $PROCESS_IDS
fi

# Don't restart process if argument is 'stop'
if [ "$1" = stop ]; then
	exit
fi

# Start process
if [ $(whoami) = taco ]; then
	su $USER
fi
# cd ~/anchorAnalytics
exec ./$SCRIPT 1> $OUTPUT 2> $ERROR &
