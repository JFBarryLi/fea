run-api:
	uvicorn api.main:fea_app --reload --host=0.0.0.0 --port=80

test:
	pytest -vv

build:
	docker build -t fea-app .

docker-run:
	docker run -d --name fea-app fea-app:latest
