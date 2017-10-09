"""
This script will combine clade specific phylogenies with a backbone tree.
It will use all the tree files ending in `.tre` in a directory, in the order they
are in.

The process is iterative, the first step is to combine the backbone tree (the 
filename must begin with `1_`) with one of the clade specific phylogenies
and to produce a combined phylogeny. Then, this combined phylogeny is used as the
backbone to add a second clade specific phylogeny and in turn, produces a second, 
and larger combined phylogeny. The process goes on until there are no more clade 
specific trees to add.

This approach uses the `combine_trees.py` script included with PyPHLAWD. However, 
I've noticed that the size of the resulting combined tree changes depending on 
the order in which the backbone and clade specific phylogenies are passed to it. 
This curent script will run `combine_trees.py` twice, once with the backbone passed 
as the first argument and a once as the second argument. It will then pick the 
resulting combined tree with the most taxa. If both trees have the same number of
tips, it will pick the first one.

Requires phyx to be installed in the path, the PyPHLAWD script `combine_trees.py` 
and the modules within it, and the script `Check_MRCA.sh` to all be in the same
directory.

Written by Simon Uribe-Convers - October 6th, 2017 - http://simonuribe.com

"""

import sys
import os
import glob
import combine_trees
import __future__

os.system("./Check_MRCA.sh")

sys.stdout = open("Info.log", "a")
sys.stderr = open ("Error.log", "w")

# Run first iteration
if os.path.exists("combined_backbone.tre"):
    os.remove("combined_backbone.tre")

if os.path.exists("combined_clade.tre"):
    os.remove("combined_clade.tre")

os.system("mkdir Combined_Tree_Stats")


trees = ""
for i in glob.glob("*.tre"):
    trees = trees + i + " "

trees

tree_list = trees.strip().split(" ") 
tree_list
backbone_tree = tree_list[0]

for i in tree_list[1:]:
    cmd_combine_back = "python combine_trees.py " + backbone_tree + " " + i + " > combined_backbone.tre"
    os.system(cmd_combine_back)
    
    cmd_combine_clade = "python combine_trees.py " + i + " " + backbone_tree + " > combined_clade.tre"
    os.system(cmd_combine_clade)
    
# Run phyx on both combined trees
    
    cmd_backbone = "pxlstr -t combined_backbone.tre -n > combined_backbone_first.txt ; cp combined_backbone_first.txt Combined_Tree_Stats/combined_backbone_first.txt" + "_" + i + ".txt"
    cmd_clade = "pxlstr -t combined_clade.tre -n > combined_clade_first.txt ; cp combined_clade_first.txt Combined_Tree_Stats/combined_clade_first.txt" + "_" + i + ".txt"
    
    os.system(cmd_backbone)
    os.system(cmd_clade)
    
# Read in files produced by phyx
    t1 = open("combined_backbone_first.txt", "r")
    comb_backbone = int(t1.read().strip())
    t1.close()
    
    t2 = open("combined_clade_first.txt", "r")
    comb_clade = int(t2.read().strip())
    t2.close()
    
    if comb_backbone >= comb_clade:
        os.remove("combined_clade.tre")
        os.rename("combined_backbone.tre", "backbone.tre")
    else:
        os.remove("combined_backbone.tre")
        os.rename("combined_clade.tre", "backbone.tre")
    backbone_tree = "backbone.tre"
    print("\n~~~~~~~~\n\nThe last clade added was %s\n\n~~~~~~~~\n\n" %i)
    os.system("sleep 3")


os.system("mv backbone.tre Final_Combined.tre")
os.system("echo Your final combined tree has the following number of tips: >> Info.log")
os.system("pxlstr -t Final_Combined.tre -n >> Info.log")
os.system("mkdir Results_Tree_Combiner; mv *.tre combined* Combined* NO* phyx* Error.log Info.log ./Results_Tree_Combiner")
