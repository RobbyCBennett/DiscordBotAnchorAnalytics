#!/bin/sh

# Config
USER='discord'
NAME='discord-bot-anchor-analytics'
OUTPUT='log/log.log'
ERROR='log/err.err'

# Stop
if [ "$1" = stop ]; then
	if [ `pidof $NAME -s` ]; then
		pkill $NAME
	else
		echo "No program started with name '$NAME'"
		exit 1
	fi
# Start
else
	if [ `whoami` = taco ]; then
		su $USER
	fi
	cd ~/anchorAnalytics
	exec -a $NAME "./bot.py & 1> $OUTPUT 2> $ERROR"
fi
