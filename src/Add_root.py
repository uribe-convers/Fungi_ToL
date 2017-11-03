"""
This script will take a phylogeny and attach it to another phylogeny. 
The resulting tree will have these two phylogenies as sister clades, and one
of them can serve as the outgroup.

Simon Uribe-Convers - November 02, 2017 - http://simonuribe.com
"""

import sys
import __future__


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python "+sys.argv[0]+" tree1 tree2 output_tree")
        print("Not enough arguments, bye!")
        sys.exit(0)


t1 = open(sys.argv[1], "r")
t2 = open(sys.argv[2], "r")
t3 = open(sys.argv[3], "w")

tree1 = t1.readlines()
tree1[0] = "(" + tree1[0] + "),"
tree1 = tree1[0].replace(";", "")

tree2 = t2.readlines()
tree2 = "(" + tree2[0] + ")"
tree2 = tree2.replace(";", "")

tree3 = "(" + tree1 + tree2 + ");"

t3.write(tree3)
