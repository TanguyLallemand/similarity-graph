#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB

# To get list of possible arguments and their effects please call script wit -h or --help argument

# Import library containing all functions written for this project
from lib import library
# Permit to access to arguments passed to python script
import sys
# Permit to perform regular expressions
import re
# Module permitting to get current directory
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-a", "--all", help="Ask script to get all fasta files from current directory", action="store_true")
# Store path or filename given as a list
parser.add_argument(
    "-f", "--file", help="Give a path or filename of a fasta file", action='append')
parser.add_argument("-e", "--concatenate",
                    help="Concatenate graphs from different fasta files into one graph", action="store_true")
# Wait for a number, if nothing is given add a default value
parser.add_argument("-c", "--threshold", help="Give a numeric value as threshold to select or not an alignement",
                    type=float, nargs='?', default=100)
parser.add_argument(
    "-d", "--default", help="Let script choose for output file and directory names", action="store_true")
parser.add_argument(
    "-p", "--png", help="Ask to save output graph in png", action="store_true")
parser.add_argument(
    "-m", "--pdf", help="Ask to save output graph in pdf", action="store_true")
parser.add_argument("-i", "--interactive",
                    help="Ask to display an interactive graph in a web browser with D3.js", action="store_true")

args = parser.parse_args()

# Initialization of some variables
filename = ''
files_to_compute = ''
dico_fasta = {}
nodes = []
edges = []
# Get threshold given as argument
cut_off = args.threshold
# If -a or --all argument is detected, this script will search in current directory all fasta files
if args.all:
    # Search for all fasta file(s) in current directory
    files_to_compute = library.getFastaFiles()
    if files_to_compute:
        # Verbose for user
        print('Script will work on thoses files: \n')
        # Print all fasta files detected
        for files in files_to_compute:
            print(files)
        print('\n')


if args.file:
    # Save filename given as a list
    files_to_compute = args.file

# If no informations were passed to script, he try to get a fasta file in current directory
if dico_fasta == {} and not files_to_compute:
    # Get path where script is executed
    cwd = os.getcwd()
    # Inform user what script will do
    print('You don\'t ask for anything, script will display all fasta files from current directory ' + cwd + '\n')
    # Try to get a fasta file from current directory
    files_to_compute = library.getFastaFiles()
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
    dico_fasta = library.getFasta(file)
    # Alignment of sequences from fasta file
    alignments = library.alignSequences(dico_fasta, args, file, cut_off)
    # Parsing of results

    # If user ask to concatenate graphs
    if args.concatenate:
        nodes += alignments[0]
        edges += alignments[1]
    # Else a different graph is construct for each fasta file
    else:
        nodes = alignments[0]
        edges = alignments[1]

    # Create a networkX graph object
    G = library.createGraph(nodes, edges)
    # Function that will save and display graph as user ask. Script will give informations for user
    library.displayAndSaveGraph(args, file, cut_off, G)

print('Job done, script will exit')
