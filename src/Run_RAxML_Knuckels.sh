#!/bin/bash

# Simple script to call RAxML after pyPHLAWD has finished
# It will also remove possible "knuckles" in the constraint tree (requires Phyx)
# Simon Uribe-Convers - August 25, 2017 - http://simonuribe.com

ALN=*outaln
knuckles=*outaln.constraint.tre

pxrmk -t $knuckles -o $(echo $knuckles)"_no_knuckles.tre"


raxmlHPC-PTHREADS-AVX -T 15 -p 9876 -m GTRCAT -q *_outpart -g *outaln.constraint.tre_no_knuckles.tre -s $ALN -n $(echo $ALN)"_450bp.tre"
