#!/bin/bash

# Simple script to call RAxML after pyPHLAWD has finished
# Simon Uribe-Convers - August 25, 2017 - http://simonuribe.com

ALN=*outaln

raxmlHPC-PTHREADS-AVX2 -T 15 -p 9876 -m GTRCAT -q *_outpart -g *outaln.constraint.tre -s $ALN -n $(echo $ALN)".tre"
