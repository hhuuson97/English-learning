run-local:
	bazel build english_learning_bin
	HOST=127.0.0.1;USERNAME=sonhh;PASSWORD=mtk10197 bazel run english_learning_bin
gazelle:
	bazel run //:requirements.update
	bazel run //:gazelle_python_manifest.update
	bazel run //:gazelle
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