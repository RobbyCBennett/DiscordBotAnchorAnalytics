python-exists:
	@which python > /dev/null

pip-exists:
	@which pip > /dev/null

install: python-exists pip-exists
	pip install --upgrade pip
	pip install python-dotenv aiohttp discord
	sudo cp -r . /usr/local/src/discord-bot-anchor-analytics
	cd /usr/local/src/discord-bot-anchor-analytics
	sudo cp discord-bot-anchor-analytics.service /etc/systemd/system/discord-bot-anchor-analytics.service
	sudo systemctl daemon-reload
	sudo systemctl enable discord-bot-anchor-analytics
	sudo systemctl start discord-bot-anchor-analytics
