# Soar-Python-Minimum-Working-Example
A minimum working example for using the SOAR cognitive architecture with python for creating an agent that interacts with the environment using SOAR's input-output links.

# How to start

On a linux machine:

1) Install java OpenJDK v8

2) Install python 2 and python 3 
2.1) Make python 3 your default option by adding this to .bashrc:

	alias python=python3

3) Install swig
	
	sudo apt install swig

4) Clone Soar from github: 

	git clone https://github.com/SoarGroup/Soar.git

5) At Soar's root folder, run python build script: 

If you want to use python 2, run this:

	python scons/scons.py sml_python

However, if you want to use python 3, run the following:

	python2 scons/scons.py sml_python --python=/usr/bin/python3
  
Build results should be in folder /out
  

## Run hello-world to see if it is working

At a terminal, export LD_LIBRARY_PATH and PYTHONPATH to Soar's code current location, for instance:

	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/Desktop/Soar/out
	export PYTHONPATH=$PYTHONPATH:~/Desktop/Soar/out

An alternative is to copy those lines to the end of .bashrc file, so you don't have to do it every time you open a new terminal.

Run hello world example:

	python hello-world.py 

You should see the following:

	Hello world
	1:    ==>S: S2 (state no-change)  

## Run toy-env.py for an example of using IO

Run the toy environmnet example:

	python toy-env.py
 
You should see something like this:

	(' ------------- Soar cycle: ', 0, ' ------------- ')
	('---> Environment sensed: ', [7, 9])
	===> Soar output: 16.000000
	
	===> Soar input: 7.000000 9.000000
	1:    O: O2 (initialize-toy-env)
	('---> Environment acted:', 0)
	(' ------------- Soar cycle: ', 1, ' ------------- ')
	('---> Environment sensed: ', [7, 3])
	===> Soar output: 10.000000
	
	===> Soar input: 7.000000 3.000000
	2:    ==>S: S2 (state no-change)
	('---> Environment acted:', 16.0)
	(' ------------- Soar cycle: ', 2, ' ------------- ')
	('---> Environment sensed: ', [3, 4])
	===> Soar output: 7.000000
	
	===> Soar input: 3.000000 4.000000
	3:    ==>S: S3 (state no-change)
	('---> Environment acted:', 10.0)
	soar> 

The goal of this exercise is to show how to use the IO interface and perform a simple cognitive cycle inside a Soar agent.
The "toy environment" is just a function that produces two random numbers and receives a single result.
This agent receives these numbers through "sensors", add them up, and return them through actuators.

# Learn more at

1) Soar Manual http://soar.eecs.umich.edu/downloads/Documentation/SoarManual.pdf

2) Soar Tutorials https://soar.eecs.umich.edu/articles/downloads/soar-suite/228-soar-tutorial-9-6-0

3) Python Interface Example https://soar.eecs.umich.edu/articles/downloads/examples-and-unsupported/183-python-interface-example

4) Python SML Interface file /Soar/build/Core/ClientSMLSWIG/Python/Python_sml_ClientInterface.py 

5) pysoarlib https://github.com/amininger/pysoarlib


  
