all: venv
	venv/bin/pip install -e .
ifneq ($(wildcard requirements.txt),) 
	venv/bin/pip install -r requirements.txt
endif
	make clean
clean: 

test: all  
	sh -c '. venv/bin/activate; nosetests --exe'

venv: 
	virtualenv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade setuptools 
