run:
	pipenv run uvicorn --port 8080 app:app

run-development:
	pipenv run uvicorn --port 8080 app:app --reload

