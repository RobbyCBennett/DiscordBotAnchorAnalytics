python-exists:
	@which python > /dev/null

pip-exists:
	@which pip > /dev/null

install: python-exists pip-exists
	pip install --upgrade pip
	pip install python-dotenv discord
	@make update

update:
	sudo git pull
	@if [ $$PWD != /usr/local/src/discord-bot-anchor-analytics ] ; then \
		sudo cp -r . /usr/local/src/discord-bot-anchor-analytics ; \
		cd /usr/local/src/discord-bot-anchor-analytics ; \
	fi
	sudo cp discord-bot-anchor-analytics.service /etc/systemd/system/discord-bot-anchor-analytics.service
	sudo systemctl daemon-reload
	sudo systemctl enable discord-bot-anchor-analytics
	sudo systemctl start discord-bot-anchor-analytics

status:
	sudo systemctl status discord-bot-anchor-analytics

start:
	sudo systemctl start discord-bot-anchor-analytics

stop:
	sudo systemctl stop discord-bot-anchor-analytics

restart:
	sudo systemctl restart discord-bot-anchor-analytics
