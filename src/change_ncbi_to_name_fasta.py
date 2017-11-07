"""This script will change NCBI IDs to species names

Simon Uribe-Convers - November 07th, 2017 - http://simonuribe.com"""

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python "+sys.argv[0]+" table infile outfile"
        sys.exit(0)
    
    tab = open(sys.argv[1],"r")
    fasta = open(sys.argv[2], "r")
    outf = open(sys.argv[3],"w")
    
    # Dictionary with NCBI IDs as keys and species names as values
    idn = {}
    for i in tab:
        spls = i.strip().split("\t")
        idn[spls[1]] = spls[4]
    tab.close()
    
    # Function to search and replace all keys for values in the dictionary
    def replace_all(text, dictionary):
        for i, j in iter(dictionary.items()):
            text = text.replace(i, j)
        return text

    # Read in data
    data = fasta.read()

    # Replace patterns and write output
    data_new_names = replace_all(data, idn)
    data_new_names = data_new_names.replace(" ","_")
    outf.write(data_new_names)
    outf.close()
