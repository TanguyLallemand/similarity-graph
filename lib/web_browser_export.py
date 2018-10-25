# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB

# Library of function for handling with web exportation in python_align project

###############################################################################
# This function will create a json using G object from networkX
###############################################################################


def createJSON(G, width, height, title):
    import json
    from networkx.readwrite import json_graph

    # Prepare data to write in jsonFile
    data = {}
    # Add output graph's title
    data['title'] = title
    # Add graph informations to object in construction
    data.update(json_graph.node_link_data(G))
    # write json formatted data
    # Source : https://networkx.github.io/documentation/stable/reference/readwrite/generated/networkx.readwrite.json_graph.node_link_data.html#networkx.readwrite.json_graph.node_link_data
    # Open in write mode json file
    with open('export_in_d3/network_graph_data.json', 'w') as jsonFile:
        # Write data in json file
        jsonFile.write(json.dumps(data, indent=4))

    print('Json saved in ./export_in_d3/network_graph_data.json \n')

###############################################################################
# This function permit to open a web browser to display json datas
###############################################################################


def displayD3(name):

    # Source: https://stackoverflow.com/questions/22004498/webbrowser-open-in-python
    # Open network_graph.html with a web browser to display network graph using JavaScript
    import webbrowser
    import os
    webbrowser.open('file://' + os.path.realpath(name))
