.PHONY: install test run docker
install: ; pip install -e ".[dev]"
test: ; pytest -q
run: ; python -m app
docker: ; docker build -t cognis/app:local .
