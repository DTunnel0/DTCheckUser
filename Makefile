clean:
	@echo 'Cleaning up...'
	rm -rf build dist *.egg-info
	rm -rf *.spec
	rm -rf ./virtualenv

build:
	$(MAKE) clean

	@echo 'Building...'
	python setup.py build

install:
	$(MAKE) clean

	@echo 'Installing...'
	python setup.py install