#!/bin/bash

conda create --name python_align --file ./Packages_used_for_virtual_env/python_environment_used.txt
source activate python_align
chmod +x ../python_align.py
../python_align.py -f ../example_of_fasta_files/sequence.fasta -d
