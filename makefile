# $Id$
# Makefile for ppl

.PHONY: all build test clean

build:
	virtualenv .
	bin/python setup.py develop

clean:
	rm -Rf bin man build include lib .Python ppl.egg-info

test: bin/nosetests
	bin/nosetests -s ppl

bin/nosetests: bin/python
	bin/pip install nose
	touch bin/nosetests

