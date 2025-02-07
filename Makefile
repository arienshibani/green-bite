.DEFAULT_GOAL := help

## Install dependencies required for the project.
install:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	python -m nltk.downloader punkt averaged_perceptron_tagger

## Run the API.
start:
	echo "Starting API at 👉 http://localhost:80/docs 👈"
	. venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 80

test:
	. venv/bin/activate && pytest && flake8

help:
	@echo "Available commands 📚"
	@echo "----------------------"
	@echo "make install - Install dependencies required for the project."
	@echo "make start - Start the API."
	@echo "make test - Run unit-tests and lint all .py files with flake8."

build:
	docker build -t green-bite .