# Scan current directory searching for fasta files
def getFastaFiles():
    # Import glob module specialized in searching files following patterns.
    # Source: https://docs.python.org/2/library/glob.html
    import glob
    # Search for files ending with fasta extensions
    fasta_files = glob.glob('./*.fasta')
    fasta_files += glob.glob('./*.fa')
    return fasta_files

# Open a fasta file and extract headers and associated sequences


def getFasta(file):
    # Open a file given in argument in mode read only
    nameHandle = open(file, 'r')
    # Generate a dictionnary that will contain all data from file
    fastas = {}
    # Read line by line file opened
    for line in nameHandle:
        # Check if > character exist to check if line is a header or a sequence
        if line[0] == '>':
            # Get header
            header = line[1:]
            # Intialize a new entry in dictionnary with header as key and a empty value
            fastas[header] = ''
        else:
            # Get sequence associated to header and stock it in dictionnary previously intialised
            fastas[header] += line
    # Close file
    nameHandle.close()
    # Return a dictionnary containing all data from fasta file
    return(fastas)

# Function to align sequences by pair using pairwise and get score of this alignements
# return dictionnary containning names of sequences aligned and associated score


def alignSequences(dico_fasta):
    """
    Import pairwise, permitting alignement from Biopython package.
    Understanding functions of this package
        Source: http://biopython.org/DIST/docs/api/Bio.pairwise2-module.html
    For configurations:
        Source: https://towardsdatascience.com/pairwise-sequence-alignment-using-biopython-d1a9d0ba861f
        Source: https://www.kaggle.com/mylesoneill/pairwise-alignment-using-biopython

    Pairwise permit to perform global or local alignement. For this script we choose to work using global alignements. In fact, we want to know if sequences are globally similar. Local alignements are mostly used to search for subsequences similar between to sequences.
    So for this script we use global alignement. We need to configure function to perform alignement as wanted.
    To do it we can give two coded parameters to alignement. First parameter setup matches and mismatchse. Here are possible codes:

    CODE  DESCRIPTION
    x     No parameters. Identical characters have score of 1, else 0.
    m     A match score is the score of identical chars, else mismatch
          score.
    d     A dictionary returns the score of any pair of characters.
    c     A callback function returns scores.

    The gap penalty parameters are:

    CODE  DESCRIPTION
    x     No gap penalties.
    s     Same open and extend gap penalties for both sequences.
    d     The sequences have different open and extend gap penalties.
    c     A callback function returns the gap penalties.

    For this script we select a match score for identical chars else it is a mismatch score (m code) and gap penalties for both sequences (s code too)
    For calculating score, we can supplementary parameters.
    Match score: 2
    Mismatch score: -1
    Opening Gap: -0.5
    Extending Gap: -0.1


    """
    from Bio import pairwise2
    # Generate dictionnary in order to save results
    edges = []
    nodes = []
    cut_off = 100
    # Select a sequences from dictionnary containning all sequences extracted from fasta files
    for key in dico_fasta.keys():
        # Select another sequences from dictionnary containning all sequences extracted from fasta files
        for keys2 in dico_fasta.keys():
            # Check if comparison is not already done and if sequences are different
            if (keys2 + key) not in edges and key != keys2:
                align = pairwise2.align.globalms(
                    dico_fasta[key], dico_fasta[keys2], 2, -1, -.5, -.1, score_only=True)

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
    # Get nodes positions, using graphviz_layout rather than spring_layout(). It permit to have less overlap, and less non aesthetic spacesself. Moreover, different layout programms can be used. We choosed neato
    # Source: https://stackoverflow.com/questions/48240021/alter-edge-length-and-cluster-spacing-in-networkx-matplotlib-force-graph
    pos = graphviz_layout(G, prog='neato')
    # Draw nodes
    # This function can receive different parameter and setup as wanted nodes. It is possible to change node's shape or color (using matplolib's color designation), add labels, transparency (with alpha parameter)
    nx.draw_networkx_nodes(G, pos, node_size=25, node_color="teal",
                           node_shape="s", alpha=0.5, linewidths=40, label=True)
    # Draw edges
    # This function can receive different parameter and setup as wanted edges. It is possible to change edge color, style and transparency (with alpha parameter)
    nx.draw_networkx_edges(G, pos, with_labels=True, width=5,
                           edge_color="silver", style="solid", alpha=0.5)
    # Legendes des noeuds et liens, taille et couleur controlées par font_size et font_color
    # Permit to save score as labels for edges
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(
        G, pos, font_size=9, alpha=0.5, font_color='black', edge_labels=labels)
    nx.draw_networkx_labels(G, pos, node_size=100,
                            font_size=9, font_color="grey", font_weight="bold")

    # Return graph object constructed
    return G


# Function to help user to choose what he want to do with graph. This function permit to save graph as a pdf file too.


def displayAndSaveGraph():
    # Creation of a pdf graph
    import matplotlib.pyplot as plt
    #Preparation of graph

    # Hide axis on output graph
    plt.axis('off')
    # Ask user for pdf's name
    name = input(
        'Please give a name for output file \n')
    #Add extension for output file
    name = name + '.png'
    #Get graph configuration
    # Source: https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/AdjustingImageSize.html
    #Get resolution
    dpi = plt.gcf().get_dpi()
    #Get height and width
    height, width = plt.gcf().get_size_inches()
    #Double height and width of graph
    plt.gcf().set_size_inches(height*2, width*2)
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
            plt.savefig(name, format="png",
                        bbox_inches="tight", bbox_extra_artists=[])
        except:
            print('Can\'t save graph \nPlease correct name of pdf')
    else:
        # A try block to try to save graph in pdf in maximum quality
        try:
            #plt.savefig(name + '.pdf', bbox_inches='tight', pad_inches=0)
            plt.savefig(name, format="png",
                        bbox_inches="tight", bbox_extra_artists=[])
        except:
            print('Can\'t save graph \nPlease correct name of pdf')
    # User can display immediatly graph if desired
    choice = input('Graph {} saved sucessfully \nDo you want to display graph? (y|n) \n'.format(
        name + '.pdf'))
    if choice == 'y':
        print('Script will exit when display window is close')
        plt.show()
        #Reset graph in case of a second graph coming because of -a argument
        plt.gcf().clear()
    else:
        #Reset graph in case of a second graph coming because of -a argument
        plt.gcf().clear()
