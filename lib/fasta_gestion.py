# -*- coding: utf-8 -*-
# Author: Tanguy Lallemand M2 BB

# Library of function for handling with fasta files in python_align project


###############################################################################
# This function search fasta files in current directory
# Return list of fasta files detected
###############################################################################

def getFastaFiles(directory):
    # Import glob module to search files following patterns.
    # Source: https://docs.python.org/2/library/glob.html
    import glob
    if directory == 'local':
        # Search for files ending with fasta extensions in local directory
        fasta_files = glob.glob('./*.fasta')
        fasta_files += glob.glob('./*.fa')
    else:
        # Search for file ending with fasta extension in a given directory
        fasta_files = glob.glob(directory + '*.fasta')
        fasta_files += glob.glob(directory + '*.fa')
    # Return results
    return fasta_files

###############################################################################
# This function try to get a fasta file to work on it
# Return array of filenames to compute
###############################################################################


def getAFastaFile():
    # Module permitting to get current directory
    import os
    # Get path where script is executed
    cwd = os.getcwd()
    # Inform user what script will do
    print('You don\'t ask for anything, script will display all fasta files from current directory ' + cwd + '\n')
    # Try to get a fasta file from current directory
    files_to_compute = getFastaFiles()
    print('Script found these files in directory \n')
    # Print all fasta files detected
    for files in files_to_compute:
        print(files)
    print('\n')
    # Allows to check that files have been detected. Protection from untimely crashes
    if files_to_compute:
        # Ask user to choose between these files
        filename = input(
            'Please select one of those files or give a path to a fasta file. If leave blank script will work on first of them\n')
        # If user give a choice, save it as a list
        if filename:
            files_to_compute = [filename]
        else:
            # Get first fasta found and try to align sequences from it
            files_to_compute = [files_to_compute[0]]
            print('Script will work on ' + files_to_compute[0] + '\n')
    else:
        print('No files found in current directory, script will exit')
        exit()
    return files_to_compute


###############################################################################
# This function open a fasta file and extract headers and associated sequences
# Return a dictionary containing all datas from fasta file
###############################################################################

def getFasta(file):
    # Open in read only a file given in argument
    with open(file, 'r') as fasta_file:
        # Initialize a dictionary that will contain all data extracted from a file
        fastas = {}
        # Read line by line opened file
        for line in fasta_file:
            # Check if '>' character is present to check if line is a header or a sequence
            if line[0] == '>':
                # Get first line of header containing name, no need to save quality information etc...
                header = line[1:]
                # Intialize a new entry in dictionary with header as key and a empty value
                fastas[header] = ''
            else:
                # Get sequence associated to header and stock it in dictionary previously initialized
                fastas[header] += line
    # Return a dictionary containing all datas from fasta file
    return(fastas)
