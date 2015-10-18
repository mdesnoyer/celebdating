VENV_LIB = venv/lib/python2.7
VENV_CV2 = $(VENV_LIB)/cv2.so

GLOBAL_CV2 := $(shell /usr/bin/python -c 'import cv2; print(cv2)' | awk '{print $$4}' | sed s:"['>]":"":g)

$(VENV_CV2): $(GLOBAL_CV2) venv
	cp $(GLOBAL_CV2) $@

ifneq ($(wildcard requirements.txt),) 
	venv/bin/pip install -r requirements.txt
endif
	make clean

all: venv
	venv/bin/pip install -e .

clean: 
	rm -rf venv

test: all  
	sh -c '. venv/bin/activate; nosetests --exe'

venv: 
	virtualenv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade setuptools 
