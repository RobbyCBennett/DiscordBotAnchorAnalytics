#!/bin/sh

# Config
USER='discord'
DIR='anchorAnalytics'
OUTPUT='log.log'
ERROR='err.err'
SCRIPT='discord-bot-anchor-analytics.py'

# Stop process if already running
echo
PROCESS_ID=$(pidof python3 $SCRIPT)
if [ $PROCESS_ID ]; then
	kill $PROCESS_ID
	echo "Stopped process with id $PROCESS_ID"
fi

# Don't restart process if argument is 'stop'
if [ "$1" = stop ]; then
	exit
fi

# Start process
if [ $(whoami) = taco ]; then
	su $USER
fi
cd ~/$DIR
exec ./$SCRIPT 1> $OUTPUT 2> $ERROR &
PROCESS_ID=$(pidof python3 $SCRIPT)
echo "Started process with id $PROCESS_ID"

# System startup
if [ ! -f '/etc/network/if-up.d/discord-bot-anchor-analytics.sh' ]; then
	echo
	echo The system administrator needs to run "make enable" to run on system startup.
fi
