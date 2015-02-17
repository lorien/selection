flake:
	flake8 selection test script

test:
	run test

coverage:
	coverage erase
	coverage run --source=selection -m runscript.cli test
	coverage report -m

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

upload:
	python setup.py sdist upload

pylint:
	pylint --reports=n script test selection

.PHONY: all build venv flake test vtest testloop cov clean doc
