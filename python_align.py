#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB

# To get list of possible arguments and their effects please call script wit -h or --help argument

# Import library containing all functions written for this project
from lib import library as lib


# Initialization of some variables
filename = ''
files_to_compute = ''
dico_fasta = {}
nodes = []
edges = []
# Get argument parser
args = lib.getArguments()
# Get threshold given as argument
cut_off = args.threshold

# If -a or --all argument is detected, this script will search in current directory all fasta files
if args.all:
    # Search for all fasta file(s) in current directory
    files_to_compute = lib.getFastaFiles()
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
#Call a function to try to get a fasta file
    lib.getAFastaFile()


for file in files_to_compute:
    # Get data from fasta file(s)
    dico_fasta = lib.getFasta(file)
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
    G = lib.createGraph(nodes, edges)
    # Function that will save and display graph as user ask. Script will give informations for user
    lib.displayAndSaveGraph(args, file, cut_off, G)

print('Job done, script will exit')
