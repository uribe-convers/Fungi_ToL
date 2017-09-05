#!/bin/bash

# This script calls three diffreent Python script to summarize the sequence 
# overlap between taxa, remove tips with not sufficient overlap or ones
# that are on a very long branch, and renomaing tips

# Simon Uribe-Convers - August 25, 2017 - http://simonuribe.com

rm *_Names.tre *_Label.tre* Pruning_Stats.txt
ls -lSr

# echo "What is the name of the alignment? Should be the last one in the list above ^: "
# read ALN
echo ""
echo ""
echo "Using '*_outaln' as the alignemnt file. If there are multiple file ending"
echo "like this, or multiple RAxML analyses, this script will not work!"

ALN=*_outaln

OUTFILE=RAxML_bestTree*
echo ""
echo "Summarizing overlap and adding overlap to the branches as 'labels'"
python /home/brlab/apps/PyPHLAWD/src/summarize_overlap.py $ALN $OUTFILE > $(echo $OUTFILE)"_Label.tre"

echo ""
echo "Pruning tree"
python /home/brlab/apps/PyPHLAWD/src/prune_no_overlap.py $OUTFILE"_Label.tre"

FILERENAME=*_Label.tre_pruned.tre

echo ""
echo "Renaming tips"
python /home/brlab/apps/PyPHLAWD/src/change_ncbi_to_name_tre.py *.table $FILERENAME $(echo $FILERENAME)"_Label_Pruned_Names.tre"
echo ""
echo "Here are the number of tips on your trees, also found on the file 'Pruning_Stats.txt'"
echo ""
echo "Tree with no prunig"
pxlstr -t $OUTFILE -n 
echo "Tree with pruning"
pxlstr -t $FILERENAME"_Label_Pruned_Names.tre" -n
touch Pruning_Stats.txt
echo "Tree with no prunig" > Pruning_Stats.txt
pxlstr -t $OUTFILE -n >> Pruning_Stats.txt
echo "Tree with pruning" >> Pruning_Stats.txt
pxlstr -t $FILERENAME"_Label_Pruned_Names.tre" -n >> Pruning_Stats.txt
