# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB

# Library of functions for python_align.py

from lib import web_browser_export as webexport


###############################################################################
# This function align sequences by pair using pairwise 2 and save score of this alignment.
# It will return a dictionary containing names of sequences aligned and associated score
###############################################################################


def alignSequences(dico_fasta, args, name_of_file, cut_off):
    # Understanding functions of this package
    #     Source: http://biopython.org/DIST/docs/api/Bio.pairwise2-module.html
    # For configurations:
    #     Source: https://towardsdatascience.com/pairwise-sequence-alignment-using-biopython-d1a9d0ba861f
    #     Source: https://www.kaggle.com/mylesoneill/pairwise-alignment-using-biopython
    #
    # Import from Biopython pairwise 2 functions
    from Bio import pairwise2
    from Bio.pairwise2 import format_alignment
    # Import package to perform regular expressions
    import re
    import os
    # Generate lists in order to save results
    edges = []
    nodes = []

    print('Script will select alignments with a score above: ' + str(cut_off))
    # Select a sequence from dictionary
    for key in dico_fasta.keys():
        # Select another sequence
        for keys2 in dico_fasta.keys():
            # Check if comparison is not already done and if sequences are different
            if (keys2 + key) not in edges and key != keys2:
                # Perform alignment
                align = pairwise2.align.globalms(
                    dico_fasta[key], dico_fasta[keys2], 2, -1, -.5, -.1, score_only=True)
                # Add alignments if they are sufficiently reliable
                if align > cut_off:
                    # add tuple to alignments
                    edges.append((key, keys2, round(align, 2)))
                # Add non existent nodes in list
                if key not in nodes:
                    nodes.append(key)
                if keys2 not in nodes:
                    nodes.append(key)
    # Return dictionary containing results
    return [nodes, edges]


###############################################################################
# Function to help user to choose what he want to do with graph. This function permit to save graph as a pdf file too.
###############################################################################


def displayAndSaveGraph(args, name_of_file, G, width, height, title):
    import matplotlib.pyplot as plt
    import re
    import os

    # Check if user ask for default configuration
    if args.default:
        # Give a default directory name
        directory_choice = 'output_figures'
        # Get base name
        base = os.path.basename(name_of_file)
        name = os.path.splitext(base)[0] + '.gexf'
        # Call function that will create directory
        my_path = createDirectory(directory_choice, name)
        # Save graph in gexf
        my_path = createOutputGraph(my_path, args, G)
    else:
        # Ask user for output name
        name = input(
            'Please give a name for output file \n')
        if args.png:
            # Add png extension
            name = name + '.png'
        elif args.pdf:
            # Add png extension
            name = name + '.pdf'
        else:
            # Add pdf extension
            name = name + '.gexf'
        # Ask user for a directory to save output figure
        directory_choice = input(
            'Where do you want to save {}? \nGive a name for a sub directory \nIf leaved blank it will be saved in current directory\n'.format(name))
        my_path = createDirectory(directory_choice, name)
        my_path = createOutputGraph(my_path, args, G)

    if args.interactive:
        width = width * 2
        height = height * 2
        webexport.createJSON(G, width, height, title)
        response = input('Do you want to display it in your browser? (y|n)\n')
        if response == 'y':
            name = 'export_in_d3/network_graph.html'
            webexport.displayD3(name)
    else:
        # User can display immediately graph if desired
        choice = input('Graph {} saved successfully in {} \nDo you want to display graph? (y|n) \n'.format(
            name, my_path))
        if choice == 'y':
            print('Script will exit when display window is close')
            plt.show()
            # Reset graph in case of a second graph coming
            plt.gcf().clear()
        else:
            # Reset graph in case of a second graph coming
            plt.gcf().clear()

###############################################################################
# Function permitting to create a directory following user's instructions
# Return path of created directory
###############################################################################


def createDirectory(directory_choice, name):
    import re
    import os
    # Import errno to handle with errors during directory creation
    from errno import EEXIST
    # Get current path and add sub directory name
    # Get current directory path
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
    # If no exceptions are raised pdf is saved in new sub directory
    # First path is concatenate with pdf's name wanted
    my_path = os.path.join(my_path, name)
    return my_path

###############################################################################
# This function permit to create an output file using G object from networkX and a path. This function will return path where file was created
# Return path of saved graph
###############################################################################


def createOutputGraph(my_path, args, G):
    import matplotlib.pyplot as plt
    import networkx as nx

    # Following the user's instructions the graph is saved in a particular format
    if args.png or args.pdf:
        try:
            plt.savefig(my_path,
                        bbox_inches="tight", bbox_extra_artists=[])
        except:
            print('Can\'t save graph \n')
    else:
        try:
            nx.write_gexf(G, my_path)
        except:
            print('Can\'t save graph \n')
    return my_path
