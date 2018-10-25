###############################################################################
# Function to create a graph from reliable alignments results
# Return a graph object
###############################################################################


def createGraph(nodes, edges):
    # Understanding package:
    #   Source: https://networkx.github.io/documentation/stable/index.html
    # Improve appearance:
    #   Source: https://python-graph-gallery.com/321-custom-networkx-graph-appearance/

    from networkx.drawing.nx_agraph import graphviz_layout
    import networkx as nx
    import numpy as np
    # Creation of a graph object
    G = nx.Graph()
    # Add nodes
    G.add_nodes_from(nodes)
    # Add links between nodes
    G.add_weighted_edges_from(edges)
    # Determine strong weights. Helped by: https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
    # Arbitrary choose a score above 16 is seen as a strong link. Must be changed. This function is not so much usefull in many case but can be tweak by user following his dataset to become useful.
    strong_edge = [(u, v)
                   for (u, v, d) in G.edges(data=True) if d['weight'] > 16]
    weak_edge = [(u, v)
                 for (u, v, d) in G.edges(data=True) if d['weight'] <= 15]

    # Get nodes positions, using graphviz_layout rather than spring_layout(). It permit to have less overlap or non aesthetic spaces. Moreover, different layout programs can be used. We choose neato. This permit to generate "spring model" layouts. This layout program is good for small networks (less than 100 nodes). Neato will attempt to minimize a global energy function, permitting multi-dimensional scaling.
    # Source: https://stackoverflow.com/questions/48240021/alter-edge-length-and-cluster-spacing-in-networkx-matplotlib-force-graph
    pos = graphviz_layout(G, prog='neato')
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=25, node_color="teal",
                           node_shape="s", alpha=0.5, linewidths=30, label=True)
    # Draw edges
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

###############################################################################
# Function to custom graph adding a title and resizing it
###############################################################################


def customGraph(name_of_file, cut_off):
    import matplotlib.pyplot as plt
    import re
    import os

    # Hide axis on output graph
    plt.axis('off')
    # Generate a title
    title = 'Graph of similarity of sequences from ' + name_of_file + \
        ' aligned with Pairwise 2 and filtered with a treshold of: ' + \
            str(cut_off)
    # Add a title
    plt.title(title)

    # Get height and width of graph
    # Source: https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/AdjustingImageSize.html
    height, width = plt.gcf().get_size_inches()
    # Double height and width of graph
    plt.gcf().set_size_inches(height * 2, width * 2)
