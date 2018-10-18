#!/bin/bash

conda create --name python_align --file ./Packages_used_for_virtual_env/python_environment_used.txt
source activate python_align
chmod +x script_python.py
./script_python.py -f ./fasta_files/sequence.fasta -d
