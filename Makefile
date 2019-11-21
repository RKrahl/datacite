PYTHON = python3


build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

sdist:
	$(PYTHON) setup.py sdist

clean:
	rm -rf build

distclean: clean
	rm -f MANIFEST .version
	rm -f datacite/__init__.py
	rm -rf dist


.PHONY: build test sdist clean distclean
