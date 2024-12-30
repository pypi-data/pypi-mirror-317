PROJECT=masterpiece

all:
	@echo "nmake clean package upload html"
	@echo "git tag -a stable-0.1.6 -m \"Influx and Mqtt abstraction\""
	@echo "git push origin stable-0.1.6"

package:
	@python3 -m build

install:
	@python3 -m pip install -e .

uninstall:
	@python3 -m pip uninstall $(PROJECT)

check:
	@python3 -m twine check dist/*

upload:
	@python3 -m twine upload --repository pypi dist/* --verbose

clean:
	@python3 ./clean.py

unittest:
	@python3 -m unittest discover

pyright:
	pyright
