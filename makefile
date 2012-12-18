# $Id$
# Makefile for ppl

all: build

build:
	virtualenv --no-site-packages .
	bin/python setup.py develop

clean:
	rm -Rf bin build include lib .Python ppl.egg-info

