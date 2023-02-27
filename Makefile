# Installing & Updating
install:
	@make deps
	echo The system administrator needs to run 'make enable' to run at startup.
	@make start
update:
	git pull
	@make deps
	@make restart

# Python Dependencies
python3-exists:
	@which python3 > /dev/null
pip3-exists:
	@which pip3 > /dev/null
deps: python3-exists pip3-exists
	pip3 install python-dotenv discord -t dep -U

# Daemon
enable:
	@if ! [ "$(shell id -u)" = 0 ]; then
		@echo "You are not root. You may not have permission to edit /etc/network/if-up.d"
		exit 1
	fi
	cp discord-bot-anchor-analytics.sh /etc/network/if-up.d
disable:
	@if ! [ "$(shell id -u)" = 0 ]; then
		@echo "You are not root. You may not have permission to edit /etc/network/if-up.d"
		exit 1
	fi
	rm /etc/network/if-up.d/discord-bot-anchor-analytics.sh
start:
	./discord-bot-anchor-analytics.sh
stop:
	./discord-bot-anchor-analytics.sh stop

restart:
	@make stop
	@make start
