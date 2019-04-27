MAKEFLAGS += .silent

all:
	python manage.py runserver

shell:
	python manage.py shell

.PHONY: all shell
