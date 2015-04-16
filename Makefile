flake:
	flake8 selection test

test:
	py.test

coverage:
	py.test --cov weblib --cov-report term-missing

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

upload:
	python setup.py sdist upload

pylint:
	pylint --reports=n test selection

.PHONY: all build venv flake test vtest testloop cov clean doc
