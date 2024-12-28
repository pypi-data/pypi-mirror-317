CHAINSAW_PKG = chainsaw_
SOURCES = $(wildcard chainsaw/*.py)

.PHONY: deb pip all $(CHAINSAW_PKG) build-deb install install-deb clean

all: deb wheel
deps: deb-deps wheel-deps

deb: $(CHAINSAW_PKG)
$(CHAINSAW_PKG): build-deb
	mv ../$@* ./
build-deb: $(SOURCES)
	dpkg-buildpackage --no-sign --jobs
deb-deps: /etc/debian_version
	@sudo apt-get -qq update
	sudo apt-get install debhelper dh-python python3-all python3-setuptools pybuild-plugin-pyproject

install: install-deb
install-deb: deb
	apt install ./*.deb


wheel: build-wheel
wheel-deps: /etc/debian_version
	@sudo apt-get -qq update
	sudo apt-get install portaudio19-dev libportmidi-dev libsndfile1-dev liblo-dev python3-pip dh-python
	sudo pip3 install --upgrade --break-system-packages build twine

build-wheel: pyproject.toml $(SOURCES)
	python3 -m build

install-wheel: build-wheel
	pip3 install $(PACKAGE)*.whl

push-to-pypi: build-wheel
	twine upload dist/*

clean:
	-rm -rf $(CHAINSAW_PKG)*
	-rm -rf *.whl
	-rm -rf build/ dist/ chainsaw.egg-info/
