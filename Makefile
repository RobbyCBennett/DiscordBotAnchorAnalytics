# Installing & Updating
install:
	@make deps
	@make reload
	@make start
	@make status
update:
	git pull
	@make deps
	@make reload
	@make restart
	@make status

# Python Dependencies
python3-exists:
	@which python3 > /dev/null
pip3-exists:
	@which pip3 > /dev/null
deps: python3-exists pip3-exists
	pip3 install python-dotenv discord -t dep

# Daemon Service
reload:
	service discord-bot-anchor-analytics reload
enable:
	service discord-bot-anchor-analytics enable
disable:
	service discord-bot-anchor-analytics disable
start:
	service discord-bot-anchor-analytics start
stop:
	service discord-bot-anchor-analytics stop
status:
	service discord-bot-anchor-analytics status
restart:
	service discord-bot-anchor-analytics restart
