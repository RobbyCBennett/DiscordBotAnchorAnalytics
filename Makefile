run:
	python bot.py

python-exists:
	@which python > /dev/null

pip-exists:
	@which pip > /dev/null

install: python-exists pip-exists
	sudo pip install python-dotenv aiohttp discord
