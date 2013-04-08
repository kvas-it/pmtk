# Makefile for ppl

.PHONY: all build test clean

build:
	virtualenv .
	bin/python setup.py develop

clean:
	rm -Rf bin man build include lib .Python ppl.egg-info

test:
	nosetests -s pmtk

