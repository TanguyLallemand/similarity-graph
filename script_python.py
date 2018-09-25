#! /usr/bin/env python3
# TODO: ameliorer ce graph
# TODO: gerer le cut off??

# For every file script will execute getFasta function permitting to extract header and associated sequence and return it as a dictionnary

# You can call script with -all to ask script to scan current directory and compute all fasta files
# You can give in argument name of fasta file you want to compute

from library import *
# Permit to access to arguments passed to python script
import sys
# Get argument(s) passed as list without script name
arg_passed = sys.argv[1:]
# Initialization of variables used in conditionnals
filename = ''
files_to_compute = ''
dico_fasta = {}
# If arg_passed is not empty (and have -all or filename) enter in this block
if arg_passed:
    import re
    # If -all argument is detected, this script will search in current directory all fasta files
    if arg_passed[0] == '-all':
        # Search for all fasta file in current directory
        files_to_compute = getFastaFiles()
        # Verbose for user
        print('Script will work on thoses files: \n')
        # Print all fasta files detected
        for files in files_to_compute:
            print(files)
            print('\n')

    # Search for a fasta filename passed as script argument
    # Check if argument passed is a fasta filename
    if re.search('.fasta', arg_passed[0]) or re.search('.fa', arg_passed[0]):
        # Save file name as a list
        files_to_compute = [arg_passed[0]]

# If  no arguments were passed to script
if dico_fasta == {} and not files_to_compute:
    # Module permitting to have function to work on os and paths
    import os
    # Get path where script is executed
    cwd = os.getcwd()
    # Inform user what script will do
    print('You don\'t ask for anything script will select a fasta from current directory ' + cwd + '\n')
    # Try to get a fasta file from current directory
    files_to_compute = getFastaFiles()
    # Verbose for user
    print('Script found these files in directory \n')
    # Print all fasta files detected
    for files in files_to_compute:
        print(files)
    print('\n')
    # Ask user to choose between these files
    filename = input(
        'Please select one of those files. If leave blank script will work on first of them\n')
    # If user give a choice, save it as a list
    if filename:
        files_to_compute = [filename]
    else:
        # Get first fasta found and try to align sequences from it
        files_to_compute = [files_to_compute[0]]
        print('Script will work on ' + files_to_compute[0] + '\n')

for file in files_to_compute:
    # Get data from fasta file(s)
    dico_fasta = getFasta(file)
    # Alignement of sequences from fasta file
    alignements = alignSequences(dico_fasta)
    # Create a graph object using list_of_edges, names_of_sequences, dictionnary_of_labels
    nodes = alignements[0]
    edges = alignements[1]
    print(nodes)
    print(edges)
    G = createGraph(nodes, edges)
    # Function that will save and display graph as user ask. Script will give informations for user
    displayAndSaveGraph()

print('Job done, script will exit')
