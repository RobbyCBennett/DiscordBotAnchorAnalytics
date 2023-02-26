# Installing & Updating
install:
	@make deps
	echo The system administrator needs to create, enable, and start the service
update:
	git pull
	@make deps
	echo The system administrator needs to restart the service

# Python Dependencies
python3-exists:
	@which python3 > /dev/null
pip3-exists:
	@which pip3 > /dev/null
deps: python3-exists pip3-exists
	pip3 install python-dotenv discord -t dep
