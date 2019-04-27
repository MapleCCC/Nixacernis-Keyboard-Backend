MAKEFLAGS += .silent

all:
	python manage.py runserver

shell:
	python manage.py shell

autoformat:
	autopep8 --in-place --aggressive --aggressive --recursive .

lint:
	pylint -E **/*.py

.PHONY: all shell
