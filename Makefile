clean:
	@echo 'Cleaning up...'
	rm -rf build dist *.egg-info
	rm -rf *.spec
	rm -rf ./virtualenv

release:
	$(MAKE) clean

	@echo 'Releasing...'
	rm -rf ./executable/*

	python3 -m venv virtualenv
	./virtualenv/bin/pip install -r requirements.txt
	./virtualenv/bin/pip install gevent
	./virtualenv/bin/pip install pyinstaller
	./virtualenv/bin/pyinstaller -D -F -n checkuser -c main.py
	
	mv dist/checkuser ./executable/
	$(MAKE) clean