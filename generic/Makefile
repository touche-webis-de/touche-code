
build:
	docker build -t webis/tira-ir-starter-pyterrier:0.0.1-base -f pyterrier/Dockerfile.base .

upload:
	docker push webis/tira-ir-starter-pyterrier:0.0.1-base

run:
	docker run --rm -ti -p 8888:8888 -v ${PWD}:/workspace webis/tira-ir-baselines-pyterrier:0.0.1-base \
		jupyter-lab --allow-root --ip 0.0.0.0

