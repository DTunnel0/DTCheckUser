clean:
	@echo 'Cleaning up...'
	rm -rf build dist *.egg-info
	rm -rf *.spec
	rm -rf ./virtualenv

build:
	$(MAKE) clean

	@echo 'Releasing...'
	rm -rf ./executable/*

	python3 -m venv virtualenv
	./virtualenv/bin/pip install -r requirements.txt
	./virtualenv/bin/pip install eventlet
	./virtualenv/bin/pip install pyinstaller
	./virtualenv/bin/pyinstaller --hidden-import=dns.versioned \
								 --hidden-import=dns.tsigkeyring \
								 --hidden-import=dns.namedict \
								 --hidden-import=dns.e164 \
								 --hidden-import=dns \
								 --hidden-import=dns.asyncresolver \
								 --hidden-import=dns.asyncquery \
								 --hidden-import=dns.asyncbackend \
								 --hidden-import=eventlet.hubs.epolls \
								 --hidden-import=eventlet.hubs.kqueue \
								 --hidden-import=eventlet.hubs.selects --onefile -D -F -n checkuser -c main.py
	
	mv dist/checkuser ./executable/
	$(MAKE) clean