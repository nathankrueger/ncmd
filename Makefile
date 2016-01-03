NCMD_CLIENT_CMD=./ncmd_client.py
NCMD_SERVER_CMD=./ncmd_server.py
DEFAULT_PORT=10123

# Git stuff
co:
	git add $(FILES)

ci:
	git commit

rm:
	git rm $(FILES)

push:
	git push origin master

pull:
	git pull origin master

revert:
	git reset

repo:
	open $(GIT_REPO)

# NCMD stuff
clean:
	rm *.pyc
