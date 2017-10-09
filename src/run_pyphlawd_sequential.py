#! /usr/bin/env python

""" use this to run pyphlawd, put this in a folder that you want to run the analyses"""


import os,sys

# change the database path accordingly
database= "/data_nvme/PHLAWD_DBS/pln.db"

# change your focal clade in Clade_list
Clade_list = ["Entomophthoromycotina", "Mortierellomycotina", "Ustilaginomycotina", "Taphrinomycotina", "Kickxellomycotina", "Zoopagomycotina", "Mucoromycotina", "Glomeromycotina", "Pezizomycotina", "Saccharomycotina", "Pucciniomycotina", "Agaricomycotina"]

WORKDIR = os.getcwd()+"/"

for i in Clade_list:
	cmd_setup = "python ~/apps/PyPHLAWD/src/setup_clade.py "+i+" "+database+" . " # must use . for current directory
	print cmd_setup
	os.system(cmd_setup)
	for f in os.listdir(WORKDIR):
		if f.startswith(i) and not f.endswith(".tre"):
			clusterID = f.split("_")[1]
			outconf = open(WORKDIR+clusterID+".ctl", "a")
			outconf.write("y\nn\ny\ny\n"+database+"\n"+clusterID+"\n")
			outconf.close()
			cmd_file = clusterID+"_cmd.txt"
			cmd_goodclu = "python ~/apps/PyPHLAWD/src/find_good_clusters_for_concat.py "+f+" < "+WORKDIR+clusterID+".ctl"+" > "+cmd_file
			print cmd_goodclu
			os.system(cmd_goodclu)
			with open(cmd_file,"rU") as handle:
				for l in handle:
					if l.startswith("python"):
						cmd_filterseq = l.strip()
						Concat_aln = WORKDIR+f+"/"+f+"_outaln"
						concatin = open(WORKDIR+clusterID+"_concatIn.txt","w")
						concatin.write(Concat_aln+"\n")
						concatin.close()
						cmd_filterseq += " < "+WORKDIR+clusterID+"_concatIn.txt"
						print cmd_filterseq
						os.system(cmd_filterseq)
