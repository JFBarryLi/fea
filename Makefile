run-api:
	uvicorn api.main:fea_app --reload --host=0.0.0.0 --port=8000

test:
	pytest -vv

build:
	docker build -t fea-app .

docker-run:
	docker run -d -p 5900:5900 --name fea-app fea-app:latest
