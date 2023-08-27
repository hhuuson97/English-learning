run:
	export HOST=127.0.0.1
	export USERNAME=sonhh
	export PASSWORD=mtk10197
	python main.py
build:
	docker build -t gcr.io/english-learning-396709/english-learning .
run-docker:
	docker run \
		-e USERNAME='sonhh' \
		-e PASSWORD='mtk10197' \
		-e INSTANCE_HOST='127.0.0.1' \
		-p 5000:5000 \
		gcr.io/english-learning-396709/english-learning
run-migrate:
	docker run \
		-e USERNAME='sonhh' \
		-e PASSWORD='mtk10197' \
		-e INSTANCE_HOST='127.0.0.1' \
		-p 5000:5000 \
		gcr.io/english-learning-396709/english-learning \
		flask db upgrade heads
push:
	docker push gcr.io/english-learning-396709/english-learning