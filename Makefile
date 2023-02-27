# Public

# Installing & Updating
install: --deps start
update: --pull --deps restart

# Daemon
start: --service
	service discord-bot-anchor-analytics start
restart: --service
	service discord-bot-anchor-analytics restart
stop: --service
	service discord-bot-anchor-analytics stop
enable: --service
disable: stop
	rm /etc/systemd/user/discord-bot-anchor-analytics.service

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

# System init
--service:
	@if ( command -v openrc 1> /dev/null ); then \
		ln -s service/openrc /etc/init.d/discord-bot-anchor-analytics; \
	elif ( command -v systemd 1> /dev/null ); then \
		ln -s service/systemd.service /etc/systemd/user/discord-bot-anchor-analytics.service; \
	else \
		echo 'Platform not supported'; \
	fi

# Update repository
--pull:
	git pull

# Python dependencies
--python3:
	@command -v python3 > /dev/null
--pip3:
	@command -v pip3 > /dev/null
--deps: --python3 --pip3
	pip3 install python-dotenv discord -t dep -U
