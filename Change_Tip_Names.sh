#!/bin/bash

# Simple script to call the script that renames the tips of the tree 
# Simon Uribe-Convers - August 25, 2017 - http://simonuribe.com

OUTFILE=RAxML_bestTree*

python /home/brlab/apps/PyPHLAWD/src/change_ncbi_to_name_tre.py *.table $OUTFILE $(echo $OUTFILE)"_Names.tre"
