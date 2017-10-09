# Figuring out the intersect of leaves between two trees and the total tips a combined tree
# should have. Also, finding which leaves get thrown out with `combine_trees.py`
# Simon Uribe-Convers - Sep 07, 2017

setwd("/Users/SAI/Documents/-Projects/--PyPHLAWD/Fungi_ToL/All_Clades_BestTrees/test/")

library(geiger)
library(dplyr)

# Trees must be in Newick format, otherwise change read.tree for read.nexus

intersect.tree <- function(tree1, tree2){
  x <- read.tree(tree1)
  y <- read.tree(tree2)
  total.tip <- length(x$tip.label) + length(y$tip.label)
  intersect.length <- length((intersect(x$tip.label, y$tip.label)))
  cat("Tree1 has", length(x$tip.label), "tips.\n")
  cat("Tree2 has", length(y$tip.label), "tips.\n")
  cat("The total number of tips is:", total.tip,"\n")
  cat("The intersect between the two trees is:",intersect.length,"\n")
  cat("Combined tree should have", total.tip - intersect.length, "tips.\n")
  
  }

# Finding the ofending taxa, i.e., the ones that are in one of the two trees but that
# are not in the combined tree.
# You must first run `combine_trees.py` and use that tree as one of the input

offending.taxa <- function(tree1, tree2, combined_tree){
  x <- read.tree(tree1)
  y <- read.tree(tree2)
  z <- read.tree(combined_tree)
  xx <- as.matrix(x$tip.label)
  yy <- as.matrix(y$tip.label)
  combined <- as.matrix(z$tip.label)
  added <- unique(rbind(xx, yy))
  cat("There are", length(setdiff(added, combined)), "leaves that are not in the combined tree and they are:\n",setdiff(added, combined))

}

