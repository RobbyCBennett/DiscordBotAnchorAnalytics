# Public

# Installing & Updating
install: --deps start
update: --pull --deps start

# Daemon
start:
	./discord-bot-anchor-analytics.sh
restart: start
stop:
	./discord-bot-anchor-analytics.sh stop
enable:
	cp discord-bot-anchor-analytics.sh /etc/network/if-up.d
disable:
	rm /etc/network/if-up.d/discord-bot-anchor-analytics.sh

help:
	@echo
	@echo 'make:         install and start'
	@echo 'make install: install and start'
	@echo 'make update:  update and restart'
	@echo
	@echo 'make start:   stop process if running and start'
	@echo 'make restart: stop process if running and start'
	@echo 'make stop:    stop process if running'
	@echo
	@echo 'make enable:  enable process to run on system startup'
	@echo 'make disble:  disable process from running on system startup'



# Private

# Update
--pull:
	git pull

# Python Dependencies
--python3-exists:
	@which python3 > /dev/null
--pip3-exists:
	@which pip3 > /dev/null
--deps: --python3-exists --pip3-exists
	pip3 install python-dotenv discord -t dep -U
