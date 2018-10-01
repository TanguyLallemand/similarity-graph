# Python_align

Python_align is a python script permitting to construct a network graph based on similarity between different DNA sequences.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

In order to run this script some python packages are necessary. List of package in python environment is contained in this [file](<Packages_used_for_virtual env/python_environment_used.txt>) (You can get it in Packages_used_for_virtual env/python_environment_used.txt).

### Installing

To get a virtual environment up and running

    conda create --name <env> --file python_environment_used.txt # Create a conda environment
    source activate <env> # Activate this environment to execute script in it

Give execution rights to script and execute it

    chmod +x script_python.py
    ./script_python.py

## Use this script

You can call this script with different flags

### Flags available

To adjust what you want from script, it is possible to add some flags to script call.

List of possibles arguments and their effects:

    -a or -all to ask script to get all fasta files from current directory
    You can give as argument a name or path of a fasta file that you want to compute. Example: sequences.fasta or subdirectory\sequences.fasta
    -s or --save to save alignements in a text file
    -c to give a numeric value working as a cut off
    -d or --default to let script choose for output file and directory names
    -e or --concatenate to concatenate graphs from different fasta files into one
    -h or --help to display a help message

### Examples of call:

     ./script_python.py -a -d

to ask script to work on all fasta files with default configuration

     ./script_python.py sequences.fasta -s

 to align all sequences from sequences.fasta with default cut off (100). Alignements produced will be saved in output_sequences.txt

    ./script_python.py -a -c 200

 Execute this script on all fasta files of current directory with 200 as cut off.

### Output graphs

 Prefer pdf for keep vectorial quality
 
## Built With

-   [Anaconda](https://www.anaconda.com/) - Environment management
-   [Networkx](https://networkx.github.io/) - Used to generate network graph

## Author

-   **Tanguy Lallemand**
