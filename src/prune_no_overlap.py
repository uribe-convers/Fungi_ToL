import sys
import os
import tree_reader
import node

"""
Written by: Simon Uribe-Convers - August 28 2017 - http://simonuribe./com

This script prunes tips from a phylogeny in newick format.
It has two criteria for pruning:
1) if a single leave is on an edge longer than x
2) if there is no overalp between taxa in y sites.
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Error. Required: python "+sys.argv[0]+" .treefile + [optional] max_branch_length (default 2) + [optional] min_overlap (default 100)"
        sys.exit(0)
    
# To read a single tree

# You need the `.next()` so that the tree read (which is type generator) 
# changes to type instance (the actual tree). `tree` becomes the root node and 
# you can iterate through every node in the tree.

# to do it on the interpreter
# tree = tree_reader.read_tree_file_iter("RAxML_bestTree.Saccharomycotina_147537_outaln_450bp_min_label.tre").next()
#print tree

# If runnig as a script
tree = tree_reader.read_tree_file_iter(sys.argv[1]).next()

# Setting default values for branch length and min overlap
if len(sys.argv) == 2:
    max_branch_length = 2
    min_overlap = 100

# Setting user specified values for branch length and min overlap
if len(sys.argv) == 4:
    max_branch_length = int(sys.argv[2])
    min_overlap = int(sys.argv[3])


# if sys.argv[2] == None:
#     max_branch_length = 2
# else:
#     max_branch_length = int(sys.argv[2])
# 
# if sys.argv[3] == None:
#     min_overlap = 100
# else:
#     min_overlap = int(sys.argv[3])

tips_long_branches = []
tips_no_overlap = ""
for j in tree.iternodes():
    # print j.label
    if len(j.children) == 0: #if there are no children nodes, then it's a tip
        if j.length > max_branch_length: #if the branche length is longer than X
            #print "Long branches to prune"
            tips_long_branches.append(j.label)#print taxa with long branches for prunnig with phyx
    
    else:
        if j.label == "": # get rid of leading empty line
            print "" 
        else:
            num = float(j.label) #convert sequence overlap from str to int
            if num <= min_overlap: #if the sequence overlap is smaller than
                tips_no_overlap = tips_no_overlap + ",".join(list(j.lvsnms()))+","

tips_no_overlap = tips_no_overlap[:-1]

# print "pxrmt -t " + sys.argv[1] + " -n " + tips_long_branches + tips_no_overlap
cmd = "pxrmt -t " + sys.argv[1] + " -n " + ",".join(tips_long_branches) + "," + tips_no_overlap + " -o " + sys.argv[1]+"_pruned.tre"
os.system(cmd)

# To read many trees
    
# tips_long_branches = []
# tips_no_overlap = ""
# for i in tree_reader.read_tree_string(sys.argv[1]):
#     tree = i
#     for j in tree.iternodes():
#         # print j.label
#         if len(j.children) == 0: #if there are no children nodes, then it's a tip
#             if j.length > 2: #if the branche length is longer than X
#                 #print "Long branches to prune"
#                 tips_long_branches.append(j.label)#print taxa with long branches for prunnig with phyx
#         
#         else:
#             if j.label == "": # get rid of leading empty line
#                 print "" 
#             else:
#                 num = float(j.label) #convert sequence overlap from str to int
#                 if num <= 100: #if the sequence overlap is smaller than
#                     tips_no_overlap = tips_no_overlap + ",".join(list(j.lvsnms()))+","
# 
# tips_no_overlap = tips_no_overlap[:-1]
# 
# # print "pxrmt -t " + sys.argv[1] + " -n " + tips_long_branches + tips_no_overlap
# cmd = "pxrmt -t " + sys.argv[1] + " -n " + ",".join(tips_long_branches) + "," + tips_no_overlap + " -o " + sys.argv[1]+"_pruned.tre"
# os.system(cmd)

# for i in tree_reader.read_tree_string(sys.argv[1]):
#     tree = i
#     for j in i.iternodes:
#         print j.label
#     if len(j.children) == 0:
#         if j.length > 5:
#           print j.label
#             
#         else:
#             num = int(j.label)
#             if num < 2:
#                 print "\n".join(j.lvsnms)
