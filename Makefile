start:
	python3 -m checkuser --start

clean:
	rm -rf build dist *.egg-info

release:
	pyinstaller -D -F -n checkuser -c main.py
	mv dist/checkuser ./executable/
	rm -rf build dist *.egg-info