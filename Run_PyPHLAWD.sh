#!/bin/bash

# This script will call pyPHLAWD and ask you what clade you want to work on.
# Simon Uribe-Convers - August 25, 2017 - http://simonuribe.com

echo "What clade are you working on?"
read CLADE

#Build database
python ~/apps/PyPHLAWD/src/setup_clade.py $CLADE /data_nvme/PHLAWD_DBS/pln.db .

ls -ltr

echo "What's the clade name and it's baseid? See list above ^"
read CLADE_NUM

echo""
echo "Here is some info for the next steps"
echo ""
echo "The main database is at:"
echo "/data_nvme/PHLAWD_DBS/pln.db"
echo ""
echo "The baseid is:"
echo $CLADE_NUM | awk -F'[_]' '{print $NF}'

#Get good clades
python ~/apps/PyPHLAWD/src/find_good_clusters_for_concat.py $CLADE_NUM

mv temp.* subMSAtable mafft.out log.md.gz $CLADE.tre $CLADE_NUM

# echo "Copy paste the line from above, right after 'line for get_min'"
# read LINE_GET_MIN
# 
# echo $LINE_GET_MIN
# #The line above asks for input but my script won't wait for it...
# # Get stats
# 
# echo "Here are the stats from your alignments"
# echo ""
# echo ""
# echo "Unfiltered"
# pxlssq -s $CLADE_NUM/$CLADE_NUM"_outaln"
# echo ""
# echo ""
# echo "Filtered"
# pxlssq -s $CLADE_NUM/$CLADE_NUM"_outaln.filt"
#  
#  
# # #Build tree
# echo "Building the phylogeny"
# # 
# cd $CLADE_NUM
# 
# ls -ltr
# 
# echo "What's the name for the phylogeny? Look here ^ for options"
# read PHYLO
# 
# raxmlHPC-PTHREADS-AVX2 -T 15 -p 9876 -m GTRCAT -q $CLADE_NUM"_outpart" -g $CLADE_NUM"_outaln.constraint.tre" -s $CLADE_NUM"_outaln" -n $PHYLO
# 
# #ALN=*outaln
# 
# #raxmlHPC-PTHREADS-AVX2 -T 15 -p 9876 -m GTRCAT -q *_outpart -g *outaln.constraint.tre -s $ALN -n $(echo $ALN)"_450bp.tre"
# 
# 
# #Change names in the tree from NCBI accession numbers to species names
# #
# OUTFILE=RAxML_bestTree*
# 
# python /home/brlab/apps/PyPHLAWD/src/change_ncbi_to_name_tre.py *.table $OUTFILE $(echo $OUTFILE)"_Names.tre"
# 
# echo "Done!"
