#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB
# Library of functions for script_python.py


# This function search fasta files in current directory
def getFastaFiles():
    # Import glob module specialized in searching files following patterns.
    # Source: https://docs.python.org/2/library/glob.html
    import glob
    # Search for files ending with fasta extensions
    fasta_files = glob.glob('./*.fasta')
    fasta_files += glob.glob('./*.fa')
    # Return results
    return fasta_files

# This function open a fasta file and extract headers and associated sequences


def getFasta(file):
    # Open in read only a file given in argument
    with open(file, 'r') as fasta_file:
        # Generate a dictionnary that will contain all datas extracted from file
        fastas = {}
        # Read line by line file opened
        for line in fasta_file:
            # Check if '>' character is present permiting to check if line is a header or a sequence
            if line[0] == '>':
                # Get first line of header, no need to save quality informations etc...
                header = line[1:]
                # Intialize a new entry in dictionnary with header as key and a empty value
                fastas[header] = ''
            else:
                # Get sequence associated to header and stock it in dictionnary previously intialised
                fastas[header] += line
    # Return a dictionnary containing all datas from fasta file
    return(fastas)


# This function align sequences by pair using pairwise 2 and get score of this alignement. It will return a dictionnary containning names of sequences aligned and associated score


def alignSequences(dico_fasta, arg_passed, name_of_file):

    # TODO: Maybe use itertool to generate all possible combination? permit to avoid conditionnals

    # import itertools, sys
    # from Bio import SeqIO, pairwise2
    #
    # fasta = sys.argv[1]
    # with open(fasta, 'r') as f:
    #     seqs = []
    #     for line in f:
    #         if not line.startswith('>'):
    #             seqs.append(line.strip())
    #
    # combos = itertools.combinations(seqs, 2)
    #
    # for k,v in combos:
    #     aln = pairwise2.align.localxx(k,v)
    #     print pairwise2.format_alignment(*aln[0])

    # Import pairwise, permitting alignement from Biopython package.
    # Understanding functions of this package
    #     Source: http://biopython.org/DIST/docs/api/Bio.pairwise2-module.html
    # For configurations:
    #     Source: https://towardsdatascience.com/pairwise-sequence-alignment-using-biopython-d1a9d0ba861f
    #     Source: https://www.kaggle.com/mylesoneill/pairwise-alignment-using-biopython
    #
    # Pairwise permit to perform global or local alignement. For this script we choose to work using global alignements. In fact, we want to know if sequences are globally similar. Local alignements are mostly used to search for subsequences.
    # We need to configure global alignement function to perform alignement as wanted.
    # To do it we can give two coded parameters:
    #   - first parameter set up matches and mismatches.
    #   - second set up gaps
    # For this script, we give a match score for identical chars else it is a mismatch score (corresponding to m code). Moreover, same gap penalties for both sequences (s code) are applied.
    # For score, we can add supplementary parameters.
    # Match score: 2
    # Mismatch score: -1
    # Opening Gap: -0.5
    # Extending Gap: -0.1

    from Bio import pairwise2
    # Import package to perform regular expressions
    import re
    import os
    from Bio.pairwise2 import format_alignment
    # Generate list in order to save results
    edges = []
    nodes = []
    # Check if -c has been passed
    if re.search('-c', str(arg_passed)) or re.search('--cut_off', str(arg_passed)):
        # Get cut off passed by saving argument just after -c and transtype it into float
        cut_off = float(arg_passed[arg_passed.index('-c') + 1])
    else:
        # Give a default value for cut off if user don't ask for a particular treshold
        cut_off = 100
    print('Script will select alignments with a score above: ' + str(cut_off))
    # Select a sequence from dictionnary
    for key in dico_fasta.keys():
        # Select linked sequence
        for keys2 in dico_fasta.keys():
            # Check if comparison is not already done and if sequences are different
            if (keys2 + key) not in edges and key != keys2:
                # Perform alignement
                align = pairwise2.align.globalms(
                    dico_fasta[key], dico_fasta[keys2], 2, -1, -.5, -.1, score_only=True)
                # If user ask for save alignements using -s argument
                if re.search('-s', str(arg_passed)) or re.search('--save', str(arg_passed)):
                    try:
                        # Make a directory following path given
                        os.mkdir('output_sequences')
                    except:
                        pass
                    # Determine name of output file
                    base = os.path.basename(name_of_file)
                    # Get name without extension
                    name = os.path.splitext(base)[0]
                    # Create final path
                    name_of_output = 'output_sequences/output_' + \
                        os.path.splitext(name)[0] + '.txt'
                    # Create a output file
                    with open(name_of_output, 'w') as output:
                        for a in pairwise2.align.globalms(dico_fasta[key], dico_fasta[keys2], 2, -1, -.5, -.1):
                            output.write(format_alignment(*a))
                # Add alignements if they are sufficently reliable
                if align > cut_off:
                    # add tuple to alignements
                    edges.append((key, keys2, round(align, 2)))
                if key not in nodes:
                    nodes.append(key)
                if keys2 not in nodes:
                    nodes.append(key)
    # Return dictionnary containning results
    return [nodes, edges, cut_off]


# Function to create a graph from reliable alignements results
# Return a graph object
# Understanding package:
#   Source: https://networkx.github.io/documentation/stable/index.html
# Improve appearance:
#   Source: https://python-graph-gallery.com/321-custom-networkx-graph-appearance/


def createGraph(nodes, edges):
    from networkx.drawing.nx_agraph import graphviz_layout
    import networkx as nx
    import numpy as np
    # Creation of a graph object
    G = nx.Graph()
    # Add nodes
    G.add_nodes_from(nodes)
    # Add links between nodes
    G.add_weighted_edges_from(edges)
    # TODO: determiner ce qui est considerer comme fort ou pas
    # Determine strong weights. Helped by: https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
    strong_edge = [(u, v)
                   for (u, v, d) in G.edges(data=True) if d['weight'] > 500]
    weak_edge = [(u, v)
                 for (u, v, d) in G.edges(data=True) if d['weight'] <= 459]

    # Get nodes positions, using graphviz_layout rather than spring_layout(). It permit to have less overlap, and less non aesthetic spaces. Moreover, different layout programms can be used. We choosed neato. This permit to generate "spring model" layouts. This layout programm is good for small networks (less than 100 nodes). Neato will attempt to minimize a global energy function, permitting multi-dimensional scaling.
    # Source: https://stackoverflow.com/questions/48240021/alter-edge-length-and-cluster-spacing-in-networkx-matplotlib-force-graph
    pos = graphviz_layout(G, prog='neato')
    # Draw nodes
    # This function can receive different parameter and set up as wanted nodes. It is possible to change node's shape or color (using matplolib's color designation), add labels, transparency (with alpha parameter)
    nx.draw_networkx_nodes(G, pos, node_size=25, node_color="teal",
                           node_shape="s", alpha=0.5, linewidths=30, label=True)
    # Draw edges
    # This function can receive different parameter and setup as wanted edges. It is possible to change edge color, style and transparency (with alpha parameter)
    # Edge for strong links
    nx.draw_networkx_edges(G, pos, edgelist=strong_edge, with_labels=True, width=5,
                           edge_color="silver", style="solid", alpha=0.8)
    # Edge for weak links
    nx.draw_networkx_edges(G, pos, edgelist=weak_edge, with_labels=True, width=5,
                           edge_color="silver", style="dashed", alpha=0.5)
    # Permit to save score as labels for edges
    labels = nx.get_edge_attributes(G, 'weight')
    # Add score on graph
    nx.draw_networkx_edge_labels(
        G, pos, font_size=9, alpha=0.5, font_color='black', edge_labels=labels)
    # Write names of sequences
    nx.draw_networkx_labels(G, pos, node_size=100,
                            font_size=6, font_color="grey", font_weight="bold")

    # Return graph object constructed
    return G


# Function to help user to choose what he want to do with graph. This function permit to save graph as a pdf file too.


def displayAndSaveGraph(arg_passed, name_of_file, cut_off):
    import matplotlib.pyplot as plt
    import re
    import os

    # Hide axis on output graph
    plt.axis('off')
    # Add a title
    plt.title('Graph of similarity of sequences from ' + name_of_file +
              ' aligned with Pairwise 2 and filtered with a cut off of: ' + str(cut_off))

    # Get height and width of graph
    # Source: https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/AdjustingImageSize.html
    height, width = plt.gcf().get_size_inches()
    # Double height and width of graph
    plt.gcf().set_size_inches(height * 2, width * 2)
    # Check if user ask for default configuration
    if re.search('-d', str(arg_passed)) or re.search('--default', str(arg_passed)):
        # Give a default directory name
        directory_choice = 'output_figures'
        # Get basename
        base = os.path.basename(name_of_file)
        # Change extension by pdf
        name = os.path.splitext(base)[0] + '.pdf'
        #Call a function that will create directory and output pdf
        my_path = createDirectoryAndOutputGraph(directory_choice, name)
    else:
        # Ask user for pdf's name
        name = input(
            'Please give a name for output file \n')
        # Add extension for output file. Prefer pdf for keep vectorial quality
        name = name + '.pdf'
        # Ask user for a directory to save pdf
        directory_choice = input(
            'Where do you want to save {}.pdf? \nGive a name for a subdirectory \nIf leaved blank it will be saved in current directory\n'.format(name))
        if directory_choice:
            my_path = createDirectoryAndOutputGraph(directory_choice, name)
        else:
            # A try block to try to save graph in pdf in maximum quality
            try:
                my_path = os.getcwd() + '/' + directory_choice
                plt.savefig(name,
                            bbox_inches="tight", bbox_extra_artists=[])
            except:
                print('Can\'t save graph \nPlease correct name of pdf')
    # User can display immediatly graph if desired
    choice = input('Graph {} saved sucessfully in {} \nDo you want to display graph? (y|n) \n'.format(
        name, my_path))
    if choice == 'y':
        print('Script will exit when display window is close')
        plt.show()
        # Reset graph in case of a second graph coming because of -a argument
        plt.gcf().clear()
    else:
        # Reset graph in case of a second graph coming because of -a argument
        plt.gcf().clear()


# This function permit to create a directory and save output pdf file in it


def createDirectoryAndOutputGraph(directory_choice, name):
    import matplotlib.pyplot as plt
    import re
    import os
    # Import errno to handle with errors during directory creation
    from errno import EEXIST
    import os
    # Get current path and add subdirectory name
    # Figures out the absolute path for you in case your working directory moves around.
    my_path = os.getcwd() + '/' + directory_choice
    # Try to create a new directory
    # Source: https://stackoverflow.com/questions/11373610/save-matplotlib-file-to-a-directory/11373653#11373653
    try:
        # Make a directory following path given
        os.mkdir(my_path)
    except OSError as exc:
        if exc.errno == EEXIST:
            pass
        else:
            raise
    # If no exceptions are raised pdf is saved in new subdirectory
    # First path is concatenate with pdf's name wanted
    my_path = os.path.join(my_path, name)
    # Try to save pdf
    try:
        plt.savefig(my_path,
                    bbox_inches="tight", bbox_extra_artists=[])
    except:
        print('Can\'t save graph \n')
    return my_path

# Display help if user ask for it


def displayHelp():
    wait = input(
        'This script was designed to construct a graph a similarity between different DNA sequences\n')
    wait = input('List of possibles arguments and their effects:\n\n -a or -all to ask script to get all fasta files from current directory\n You can give as argument a name or path of a fasta file that you want to compute. Example: sequences.fasta or subdirectory\sequences.fasta\n -s or --save to save alignements in a text file\n -c to give a numeric value working as a cut off\n -d or --default to let script choose for output file and directory names\n -h or --help to display a help message\n\n Examples of call:\n./script_python.py -a -d to ask script to work on all fasta files with default configuration\n./script_python.py sequences.fasta -s to align all sequences from sequences.fasta with default cut off (100). Alignements produced will be saved in output_sequences.txt\n./script_python.py -a -c 200 Execute this script on all fasta files of current directory with 200 as cut off.\n')
    exit()
