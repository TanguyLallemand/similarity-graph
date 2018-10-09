#!/bin/bash

conda create --name python_align --file python_environment_used.txt
source activate python_align
chmod +x script_python.py
./script_python.py sequence.fasta -d
