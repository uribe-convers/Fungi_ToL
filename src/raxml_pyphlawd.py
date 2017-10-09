#! /usr/bin/env python

"""
This raxml used to run pyphlawd

"""

import os,sys
import subprocess
from seq import read_fasta_file
import random
import glob
from node import Node
import tree_reader

def listdirs(folder):
	return [os.path.abspath(d) for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

def reroot(oldroot, newroot):
	#oldroot.isroot = False
	#newroot.isroot = True
	v = [] #path to the root
	n = newroot
	while 1:
		v.append(n)
		if not n.parent: break
		n = n.parent
	#print [ x.label for x in v ]
	v.reverse()
	for i, cp in enumerate(v[:-1]):
		node = v[i+1]
		# node is current node; cp is current parent
		#print node.label, cp.label
		cp.remove_child(node)
		node.add_child(cp)
		cp.length = node.length
		cp.label = node.label
	return newroot

def remove_kink(node,curroot):
	"""
	smooth the kink created by prunning
	to prevent creating orphaned tips
	after prunning twice at the same node
	"""
	if node == curroot and len(curroot.children) == 2:
		#move the root away to an adjacent none-tip
		if curroot.children[0].istip: #the other child is not tip
			curroot = reroot(curroot,curroot.children[1])
		else: curroot = reroot(curroot,curroot.children[0])
	if node == curroot and len(curroot.children) == 1:
 		kink = node
		curroot = reroot(curroot,curroot.children[0])
		curroot.remove_child(kink)
		node = curroot
		return node, curroot
	#---node---< all nodes should have one child only now
	length = node.length + (node.children[0]).length
	par = node.parent
	kink = node
	node = node.children[0]
	#parent--kink---node<
	par.remove_child(kink)
	par.add_child(node)
	node.length = length
	return node,curroot

def raxml(DIR,cleaned,num_cores,seqtype):
	assert seqtype == "aa" or seqtype == "dna","Input data type: dna or aa"
	#assert len(read_fasta_file(DIR+cleaned)) >= 4,\
	#	"less than 4 sequences in "+DIR+cleaned
	os.chdir(DIR)
	if cleaned.endswith("_outaln.flit"):
		cladeID = cleaned.split(".")[0]
		constrainttree = cladeID+".constraint.tre.filt"
	else:
		cladeID = cleaned # unfiltered fasta
		constrainttree = cladeID+".constraint.tre"
	# remove kink for the constraint tree
	infile = open(constrainttree,"rU")
	curroot = tree_reader.read_tree_string(infile.readline().strip())
	going = True
	"""while going:
		going = False
		for i in curroot.iternodes():
			if len(i.children) == 1 and i.parent != None:
				sys.stderr.write("knuckle found")
				going = True
				ch = i.children[0]
				ch.length = ch.length+i.length
				par = i.parent
				par.remove_child(i)
				par.add_child(ch)
 				break"""
	while True:
		count = 0
		for i in curroot.iternodes():
			if not i.istip and len(i.children) == 1:
				count += 1
				node,curroot = remove_kink(i,curroot)
				break
		if count == 0:
			break
	newroot = curroot.get_newick_repr()+";"
	with open(constrainttree+".edit","w") as outfile:
		outfile.write(newroot+"\n")
	outfile.close()
	# run raxml
	partition = "_".join(cleaned.split("_")[0:2])+"_outpart"
	tree = cleaned+".raxml.tre"
	raw_tree = "RAxML_bestTree."+cleaned
	model = "PROTCATWAG" if seqtype == "aa" else "GTRCAT"
	if not os.path.exists(tree) and not os.path.exists(raw_tree):
		# raxml crashes if input file starts with . 
		cmd = ["raxmlHPC-PTHREADS-AVX2","-T",str(num_cores),"-p",str(random.randint(1,1000000)),"-s",\
			   cleaned,"-n",cleaned,"-m",model,"-q",partition,"-g",constrainttree+".edit"]
		print " ".join(cmd)
		p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
		out = p.communicate()
		assert p.returncode == 0,"Error raxml"+out[0]
		
	if os.path.exists(raw_tree):
		os.rename(raw_tree,tree)

	for file in glob.glob("RAxML_*"):
		os.remove(file)
		
	try:
		os.remove(cleaned+".reduced")
	except: pass # no need to worry about extra intermediate files

	return tree

def main(DIR,num_cores,seqtype,file_end):
	DIR = os.path.abspath(DIR)+"/"
	filecount = 0
	Direct = listdirs(DIR)
	for d in Direct:
		d = d + "/"
		for i in os.listdir(d):
			if i.endswith(file_end) and len(read_fasta_file(d+i)) >= 4:
				filecount += 1
				raxml(d,i,num_cores,seqtype)
	assert filecount > 0, "No file end with "+file_end+" found in "+DIR
	
	
if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "python raxml_pyphlawd.py DIR number_cores dna/aa file_end"
		print "make sure that the executable is named 'raxml' and is in the path"
		print "file_end either with _outaln or _outaln.filt"
		sys.exit(0)
	
	DIR, num_cores, seqtype, file_end  = sys.argv[1:]
	main(DIR,num_cores,seqtype,file_end)
	
