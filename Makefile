.PHONY: bootstrap venv deps dirs clean test release check build coverage

FILES_CHECK_MYPY = selection
FILES_CHECK_ALL = $(FILES_CHECK_MYPY) tests

bootstrap: venv deps dirs

venv:
	virtualenv -p python3 .env

deps:
	.env/bin/pip install -r requirements.txt
	.env/bin/pip install -e .

dirs:
	if [ ! -e var/run ]; then mkdir -p var/run; fi
	if [ ! -e var/log ]; then mkdir -p var/log; fi

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name '__pycache__' -delete

test:
	pytest

#release:
#	git push \
#	&& git push --tags \
#	&& make build \
#	&& twine upload dist/*

check:
	echo "mypy" \
	&& mypy --strict $(FILES_CHECK_MYPY) \
	&& echo "pylint" \
	&& pylint -j0 $(FILES_CHECK_ALL) \
	&& echo "flake8" \
	&& flake8 -j auto --max-cognitive-complexity=11 $(FILES_CHECK_ALL) \
	&& echo "bandit" \
	&& bandit -qc pyproject.toml -r $(FILES_CHECK_ALL) \

build:
	rm -rf *.egg-info
	rm -rf dist/*
	python -m build --sdist

coverage:
	pytest --cov weblib --cov-report term-missing
