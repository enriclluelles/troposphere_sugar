.PHONY: testrelease release

testrelease:
	python setup.py register -r https://testpypi.python.org/pypi
	python setup.py sdist upload -r https://testpypi.python.org/pypi

release:
	python setup.py register -r https://pypi.python.org/pypi
	python setup.py sdist upload -r https://pypi.python.org/pypi
