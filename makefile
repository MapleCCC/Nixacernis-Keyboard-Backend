MAKEFLAGS += .silent

all: server

server:
	python manage.py runserver

shell:
	python manage.py shell

preview:
	grip -b

autoformat:
	autopep8 --in-place --aggressive --aggressive --recursive .

lint:
	pylint -E **/*.py

# Use with caution!
clean:
	# Be careful this command may erase the database that's not source versioned.
	git clean -fdx

.PHONY: all server shell preview autoformat lint clean
