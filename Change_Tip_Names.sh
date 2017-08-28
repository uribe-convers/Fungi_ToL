#!/bin/bash

OUTFILE=RAxML_bestTree*

python /home/brlab/apps/PyPHLAWD/src/change_ncbi_to_name_tre.py *.table $OUTFILE $(echo $OUTFILE)"_Names.tre"
