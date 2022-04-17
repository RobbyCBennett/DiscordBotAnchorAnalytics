background:
	nohup python bot.py </dev/null >/dev/null 2>&1 &

foreground:
	python bot.py

python-exists:
	@which python > /dev/null

pip-exists:
	@which pip > /dev/null

install: python-exists pip-exists
	sudo pip install --upgrade pip
	sudo pip install python-dotenv aiohttp discord
