IMAGE_NAME ?= restful-booker-tester
PYTEST_RUN_MODE ?=

test: build
	docker run --rm $(IMAGE_NAME) $(PYTEST_RUN_MODE)

test-local:
	poetry run pytest $(PYTEST_RUN_MODE)

build:
	docker build -t $(IMAGE_NAME) .

lint:
	poetry run isort -c -d . ; poetry run yapf -dpr .; poetry run flake8 .

lint-fix:
	poetry run isort . ; poetry yapf -pir .; poetry flake8 .