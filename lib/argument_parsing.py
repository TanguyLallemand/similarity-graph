# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB

# Library of function for parsing arguments in python_align project


###############################################################################
# This function will prepare arguments
# Return argument object
###############################################################################


def getArguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--all", help="Ask script to get all fasta files from current directory", action="store_true")
    # Store path or filename of a fasta file given as a list
    parser.add_argument(
        "-f", "--file", help="Give a path or filename of a fasta file", action='append')
    # Store path of a directory
    parser.add_argument(
        "-g", "--directory", help="Give a path and script will compute all fasta files in this directory", type=str, action='store')
        # Ask script to concatenate alignements from different files into one graph
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
    return args
