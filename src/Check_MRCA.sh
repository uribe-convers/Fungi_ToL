#!/bin/bash

# This will check if the clade specfic phylogenies have a most recent common 
# ancestor (MRCA) in the backbone tree.
# Those that don't have a MRCA will be placed in a directory called NO_MRCA.
# This script is called by `Tree_Combiner.py`.

# Requires the PyPHLAWD script `combine_trees.py` and the modules within.

# Written by Simon Uribe-Convers - October 6th, 2017 - http://simonuribe.com

for i in 1_*
    do
    mv $i $(echo $i | sed 's/.tre/.txt/g')
done

mkdir NO_MRCA

for i in *.tre
    do
    python combine_trees.py 1_* $i
    if [ "$?" != "0" ]; then
        mv $i ./NO_MRCA/$i
    fi
done

for i in 1_*
    do
    mv $i $(echo $i | sed 's/.txt/.tre/g')
done
