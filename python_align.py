#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB

# To get list of possible arguments and their effects please call script wit -h or --help argument

# Import library containing all functions written for this project
from lib import library as lib
from lib import argument_parsing as arglib
from lib import fasta_gestion as faslib
from lib import graph_gestion as graphlib


# Initialization of some variables
filename = ''
files_to_compute = ''
dico_fasta = {}
nodes = []
edges = []
# Get argument parser
args = arglib.getArguments()
# Get threshold given as argument
cut_off = args.threshold

# If -a or --all argument is detected, this script will search in current directory all fasta files
if args.all:
    directory = 'local'
    # Search for all fasta file(s) in current directory
    files_to_compute = faslib.getFastaFiles(directory)
    if files_to_compute:
        # Verbose for user
        print('Script will work on thoses files: \n')
        # Print all fasta files detected
        for files in files_to_compute:
            print(files)
        print('\n')
    else:
        import sys
        print('The script does not find fasta files, please execute the script with different settings')
        sys.exit()
#If user ask for work on all file of a particular directory, enter in this conditionnal
if args.directory:
    # Save filename given as a list
    directory = args.directory
    # Search for all fasta file(s) in given directory
    files_to_compute = faslib.getFastaFiles(directory)
    if files_to_compute:
        # Verbose for user
        print('Script will work on thoses files: \n')
        # Print all fasta files detected
        for files in files_to_compute:
            print(files)
        print('\n')
#If user give a filename or a path. Could may be improved using argument_parsing function
if args.file:
    # Save filename given as a list
    files_to_compute = args.file


# If no informations were passed to script, he try to get a fasta file in current directory
if dico_fasta == {} and not files_to_compute:
#Call a function to try to get a fasta file
    faslib.getAFastaFile()


for file in files_to_compute:
    # Get data from fasta file(s)
    dico_fasta = faslib.getFasta(file)
    # Alignment of sequences from fasta file
    alignments = lib.alignSequences(dico_fasta, args, file, cut_off)
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
    G = graphlib.createGraph(nodes, edges)
    # Custom graph by adding title and resizing it
    width_and_height = graphlib.customGraph(file, cut_off)
    # Function that will save and display graph as user ask. Script will give informations for user
    lib.displayAndSaveGraph(args, file, G, width_and_height[0], width_and_height[1], width_and_height[2])

print('Job done, script will exit')
