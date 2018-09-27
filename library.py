#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB
# Library of functions for script_python.py


# This function scan current directory searching for fasta files
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
    nameHandle = open(file, 'r')
    # Generate a dictionnary that will contain all datas extracted from file
    fastas = {}
    # Read line by line file opened
    for line in nameHandle:
        # Check if '>' character is present permitting to check if line is a header or a sequence
        if line[0] == '>':
            # Get first line of header
            header = line[1:]
            # Intialize a new entry in dictionnary with header as key and a empty value
            fastas[header] = ''
        else:
            # Get sequence associated to header and stock it in dictionnary previously intialised
            fastas[header] += line
    # Close file
    nameHandle.close()
    # Return a dictionnary containing all datas from fasta file
    return(fastas)

# This function align sequences by pair using pairwise 2 and get score of this alignement. It will return a dictionnary containning names of sequences aligned and associated score


def alignSequences(dico_fasta, arg_passed, name_of_file):

    # TODO: Maybe use itertool to generate all possible combination? permit to del conditionnals

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
    # Pairwise permit to perform global or local alignement. For this script we choose to work using global alignements. In fact, we want to know if sequences are globally similar. Local alignements are mostly used to search for subsequences similar between to sequences.
    # So for this script we use global alignement. We need to configure function to perform alignement as wanted.
    # To do it we can give two coded parameters:
    #   - first parameter set up matches and mismatches.
    #   - second set up gaps
    # For this script we select a match score for identical chars else it is a mismatch score (m code) and same gap penalties for both sequences (s code too)
    # For score, we can add supplementary parameters.
    # Match score: 2
    # Mismatch score: -1
    # Opening Gap: -0.5
    # Extending Gap: -0.1

    from Bio import pairwise2
    import re
    import os
    from Bio.pairwise2 import format_alignment
    # Generate dictionnary in order to save results
    edges = []
    nodes = []
    # Check if -t has been passed
    if re.search('-t', str(arg_passed)):
        # get cut off passed by getting argument just after -t and transtype it into float
        cut_off = float(arg_passed[arg_passed.index('-t') + 1])
    else:
        # Give a default value for cut of
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
                # If user ask for save alignements
                if re.search('-s', str(arg_passed)) or re.search('--save', str(arg_passed)):
                    # Determine name of output file
                    name_of_output = 'output_' + \
                        os.path.splitext(name_of_file)[0] + '.txt'
                    # Create a output file. With permit to automatically handle file close
                    with open(name_of_output, 'w') as output:
                        for a in pairwise2.align.globalms(dico_fasta[key], dico_fasta[keys2], 2, -1, -.5, -.1):
                            output.write(format_alignment(*a))

                if align > cut_off:
                    # add tuple to alignements
                    edges.append((key, keys2, round(align, 2)))
                if key not in nodes:
                    nodes.append(key)
                if keys2 not in nodes:
                    nodes.append(key)
    # Return dictionnary containning results
    return [nodes, edges]


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
    # Add nodes. Not necessary because add_edges implicitly add nodes but if a node is not link with other node he won't be display
    G.add_nodes_from(nodes)
    # Add links between nodes
    G.add_weighted_edges_from(edges)
    # TODO: determiner ce qui est considerer comme fort ou pas
    # Determine strong weights. Helped by: https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
    strong_edge = [(u, v)
                   for (u, v, d) in G.edges(data=True) if d['weight'] > 500]
    weak_edge = [(u, v)
                 for (u, v, d) in G.edges(data=True) if d['weight'] <= 459]

    # Get nodes positions, using graphviz_layout rather than spring_layout(). It permit to have less overlap, and less non aesthetic spacesself. Moreover, different layout programms can be used. We choosed neato. This permit to generate "spring model" layouts. This is layout programm is good for small networks (less than 100 nodes). Neato will attempt to minimize a global energy function, permitting multi-dimensional scaling but non adapted to large network.
    # Source: https://stackoverflow.com/questions/48240021/alter-edge-length-and-cluster-spacing-in-networkx-matplotlib-force-graph
    pos = graphviz_layout(G, prog='neato')
    # Draw nodes
    # This function can receive different parameter and setup as wanted nodes. It is possible to change node's shape or color (using matplolib's color designation), add labels, transparency (with alpha parameter)
    nx.draw_networkx_nodes(G, pos, node_size=25, node_color="teal",
                           node_shape="s", alpha=0.5, linewidths=40, label=True)
    # Draw edges
    # This function can receive different parameter and setup as wanted edges. It is possible to change edge color, style and transparency (with alpha parameter)
    nx.draw_networkx_edges(G, pos, edgelist=strong_edge, with_labels=True, width=5,
                           edge_color="silver", style="solid", alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=weak_edge, with_labels=True, width=5,
                           edge_color="silver", style="dashed", alpha=0.5)
    # Legendes des noeuds et liens, taille et couleur controlées par font_size et font_color
    # Permit to save score as labels for edges
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(
        G, pos, font_size=9, alpha=0.5, font_color='black', edge_labels=labels)
    # Write names of sequences
    nx.draw_networkx_labels(G, pos, node_size=100,
                            font_size=6, font_color="grey", font_weight="bold")

    # Return graph object constructed
    return G


# Function to help user to choose what he want to do with graph. This function permit to save graph as a pdf file too.


def displayAndSaveGraph():
    # Creation of a pdf graph
    import matplotlib.pyplot as plt
    # Preparation of graph

    # Hide axis on output graph
    plt.axis('off')
    # Ask user for pdf's name
    name = input(
        'Please give a name for output file \n')
    # Add extension for output file. Prefer pdf for keep vectorial qualitu
    name = name + '.pdf'
    # Get graph configuration
    # Source: https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/AdjustingImageSize.html
    # Get height and width
    height, width = plt.gcf().get_size_inches()
    # Double height and width of graph
    plt.gcf().set_size_inches(height * 2, width * 2)
    # Ask user for a directory to save pdf
    directory_choice = input(
        'Where do you want to save {}.pdf? \nGive a name for a subdirectory \nIf leaved blank it will be saved in current directory\n'.format(name))
    if directory_choice or directory_choice == 'n':
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
            if exc.errno == EEXIST:  # and my_path.isdir(my_path)
                pass
            else:
                raise
        # If no exceptions are raised pdf is saved in new subdirectory
        # First path is concatenate with pdf's name wanted
        my_path = os.path.join(my_path, name)
        # Try to save pdf
        try:
            plt.savefig(name,
                        bbox_inches="tight", bbox_extra_artists=[])
        except:
            print('Can\'t save graph \nPlease correct name of pdf')
    else:
        # A try block to try to save graph in pdf in maximum quality
        try:
            #plt.savefig(name + '.pdf', bbox_inches='tight', pad_inches=0)
            plt.savefig(name,
                        bbox_inches="tight", bbox_extra_artists=[])
        except:
            print('Can\'t save graph \nPlease correct name of pdf')
    # User can display immediatly graph if desired
    choice = input('Graph {} saved sucessfully \nDo you want to display graph? (y|n) \n'.format(
        name + '.pdf'))
    if choice == 'y':
        print('Script will exit when display window is close')
        plt.show()
        # Reset graph in case of a second graph coming because of -a argument
        plt.gcf().clear()
    else:
        # Reset graph in case of a second graph coming because of -a argument
        plt.gcf().clear()

# Display help if user ask for it


def displayHelp():
    wait = input(
        'This script was designed to construct a graph a similarity between different DNA sequences\n ')
    wait = input('List of possibles arguments and their effects:\n\n -a or -all to ask script to scan current directory and compute all fasta files\n You can give as argument name of a fasta file that you want to compute\n -s or --save to save alignements in a text file\n -c to give a numeric value working as a cut off\n -h or --help to display a help message\n')
    exit()
