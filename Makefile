.PHONY: all clean test parse

TAG=$(shell git symbolic-ref -q --short HEAD)
PIPOPTIONS=--default-timeout=100

# Set a specific path for the Python executable if anaconda is the primary
# distribution on your system.
PYTHON3=python3.6

all: env/bin/python

env/bin/python:
	$(PYTHON3) -m venv env
	touch requirements.txt
	env/bin/pip install $(PIPOPTIONS) --upgrade pip
	env/bin/pip install $(PIPOPTIONS) wheel
	env/bin/pip install $(PIPOPTIONS) -r requirements.txt
	env/bin/python setup.py develop

clean:
	rm -rfv bin develop-eggs dist downloads eggs env parts
	rm -fv .DS_Store .coverage .installed.cfg bootstrap.py
	rm -fv logs/*.txt
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;

test:
	env/bin/py.test tests -vvrw

data/train.cnf:
	env/bin/treebank_to_cnf < data/train.dat > data/train.cnf

data/grammar: data/train.cnf
	env/bin/treebank_to_grammar --treebank data/train.cnf --grammar data/grammar

data/dev.parsed: data/grammar
	env/bin/parse --grammar data/grammar < data/dev.raw > data/dev.parsed

data/dev.cnf:
	env/bin/treebank_to_cnf < data/dev.dat > data/dev.cnf

evaluation.txt: data/dev.parsed data/dev.cnf
	env/bin/evaluate --gold data/dev.cnf --test data/dev.parsed > evaluation.txt

parse: data/dev.parsed

