#! /usr/bin/env python

""" use this to run pyphlawd, put this in a folder that you want to run the analyses"""
""" to run in parallel, call it with: `parallel ./run_pyphlawd_parallel.py . {} < File_with_clade`"""

import os,sys

# change the database path accordingly
database= "/data_nvme/PHLAWD_DBS/pln.db"

# change your focal clade in Clade_list
"""Clade_list = ["Apodiformes", "Bucerotiformes", "Galloanserae", "Gaviiformes","Coliiformes","Cariamiformes","Psittaciformes",\
			"Sphenisciformes", "Strigiformes", "Trochiliformes", "Musophagiformes", "Cuculiformes", "Piciformes", "Galbuliformes", \
			"Podicipediformes", "Phoenicopteriformes", "Trogoniformes", "Upupiformes", "Turniciformes", "Palaeognathae", "Procellariiformes", \
			"Opisthocomiformes"]"""

#WORKDIR = os.getcwd()+"/"

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python "+sys.argv[0]+" WORKDIR Clade_list"
		print "Clade_list separate by comma"
		sys.exit(0)
	WORKDIR = sys.argv[1]
	WORKDIR = os.path.abspath(WORKDIR)+"/"
	Clade_list = sys.argv[2].split(",")
		
	for i in Clade_list:
		os.chdir(WORKDIR)
		path = WORKDIR+i
		if not os.path.exists(path):
			os.makedirs(path)
			os.chdir(path)
			cmd_setup = "python ~/apps/PyPHLAWD/src/setup_clade.py "+i+" "+database+" . " # must use . for current directory
			print cmd_setup
			os.system(cmd_setup)
			for f in os.listdir(path):
				if f.startswith(i) and not f.endswith(".tre"):
					clusterID = f.split("_")[1]
					outconf = open(path+"/"+clusterID+".ctl", "a")
					outconf.write("y\nn\ny\ny\n"+database+"\n"+clusterID+"\n")
					outconf.close()
					cmd_file = path+"/"+clusterID+"_cmd.txt"
					cmd_goodclu = "python ~/apps/PyPHLAWD/src/find_good_clusters_for_concat.py "+f+" < "+path+"/"+clusterID+".ctl"+" > "+cmd_file
					print cmd_goodclu
					os.system(cmd_goodclu)
					with open(cmd_file,"rU") as handle:
						for l in handle:
							if l.startswith("python"):
								cmd_filterseq = l.strip()
								Concat_aln = path+"/"+f+"/"+f+"_outaln"
								concatin = open(path+"/"+clusterID+"_concatIn.txt","w")
								concatin.write(Concat_aln+"\n")
								concatin.close()
								cmd_filterseq += " < "+path+"/"+clusterID+"_concatIn.txt"
								print cmd_filterseq
								os.system(cmd_filterseq)
	
