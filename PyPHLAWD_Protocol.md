# How to run PyPHLAWD
### Simon Uribe-Convers - August 7th, 2017 - http://simonuribe.com

---

##  Structure in Smith Lab's machines and data

The plants and fungi database is in: `/data_nvme/PHLAWD_DBS/pln.db`

All the scripts are in: `~/apps/PyPHLAWD/src`

## Main arguments 

The main arguments of PyPHLAWD can be set in: `~/apps/PyPHLAWD/src/conf.py`  

**The main ones to change are:**

- smallest_size: gets rid of small genes, that are usually barcodes and/or uninformative

In BLAST bits   

- length\_limit: how much of the genes need to overlap  
- perc\_identity: how similar the genes need to be

## Building a database

**For an automated way to do all this, read the last paragraph of this section**

The first step is to build a database for the clade or species you are interested in. However, to be able to do this you'll need the NCBI data first. To download and create the NCBI database check PyPHLAWD's page [here](https://github.com/FePhyFoFum/PyPHLAWD) and then come back to _this_ tutorial.

With your NCBI database ready, type the following: `python ~/apps/PyPHLAWD/src/setup_clade.py Clade_of_Interest GenBank_Database Location_to_Build`

Example:
`python ~/apps/PyPHLAWD/src/setup_clade.py Orobanchaceae /data_nvme/PHLAWD_DBS/pln.db .`

After the database has been built, you'll need to get the good clusters only with: `python ~/apps/PyPHLAWD/src/find_good_clusters_for_concat.py Clade_of_Interest_number_attached`

Example:  
`python ~/apps/PyPHLAWD/src/find_good_clusters_for_concat.py Orobanchaceae_91896/`

It will ask you some things, following the Orobanchaceae example above:

```
Do you want to rename these clusters? y/n/# y
Do you want to make trees and trim tips for these gene regions? y/n n
Do you want to concat? y/n y
Do you want to make a constraint? y/n y
Where is the DB? /data_nvme/PHLAWD_DBS/pln.db
What is the baseid? 91896
line for get_min
python ~/apps/PyPHLAWD/src/get_min_overlap_multiple_seqs.py Orobanchaceae_91896/Orobanchaceae_91896_outaln.constraint.tre Orobanchaceae_91896/clusters/
cluster29.aln.rn Orobanchaceae_91896/clusters/cluster370.aln.rn Orobanchaceae_91896/clusters/cluster428.aln.rn Orobanchaceae_91896/clusters/cluster355.
aln.rn Orobanchaceae_91896/clusters/cluster442.aln.rn Orobanchaceae_91896/clusters/cluster413.aln.rn
```
If you copy and paste the last line (`python ~/app...get_min_overlap_multiple_seqs.py...`) it will reduce the amount of clusters based on some criteria. One of them is that taxa have to have at least two genes. If you want to ignore some genes so that you keep them regardless of how many taxa have information for them, add an underscore and the name or number for the gene, e.g., `_Orobanchaceae_91896/clusters/cluster370.aln.rn`.  

**Important,** when asked for the "Concat aln filename:", give the name that was produced by the `find_good_clusters_for_concat.py` script, not a _new_ name! For the above example it would be: `Orobanchaceae_91896/Orobanchaceae_91896_outaln`. This will produce a filtered file in `Orobanchaceae_91896/Orobanchaceae_91896_outaln.filt`.

You can see how many sequences there are in the alignments and in the filtered alignment with: `pxlssq -s Orobanchaceae_91896/Orobanchaceae_91896_outaln` and `pxlssq -s Orobanchaceae_91896/Orobanchaceae_91896_outaln.filt`, respectively.

### Automated way

Ning Wang wrote a python script to do all these steps automatically. There is a sequential and a parallel version. The scripts are called `run_pyphlawd_sequential.py` and `run_pyphlawd_parallel.py`, respectively. For the parallel version, you will need a file with the names oif the taxa that you are running (one per line) and you run it like this: `parallel ./run_pyphlawd_parallel.py . {} < file_with_names`

## Phylogenetics

Build a tree with the alignment (or filtered alignment) using partitions for each region and topological constraints but no bootstrap:

`raxmlHPC-PTHREADS-AVX2 -T 15 -p 9876 -m GTRCAT -q Orobanchaceae_91896_outpart -g Orobanchaceae_91896_outaln.constraint.tre -s Orobanchaceae_91896_outaln -n Orobanchaceae_450bp_min`

`raxmlHPC-PTHREADS-AVX2 -T 15 -p 9876 -m GTRCAT -q *_outpart -g *_outaln.constraint.tre -s`

**Important,**: if RAxML complains about the constraint tree not having branch lengths, remove the first and last parentheses in the constraint tree and try again. Continue deleting parentheses (first and last) until it works.

This will produce a tree with NCBI's accessions at the tips. To change the tips to species names do: `python /home/brlab/apps/PyPHLAWD/src/change_ncbi_to_name_tre.py *.table treefile new_treefile`

## Assess the results

You are dealing with data available publicly that have been generated by many researchers. Unfortunately, not all data available on GenBank is good, in fact, there are a lot of sequences that are wrong. Common mistakes include taxonomic misidentification, wrong gene/locus information, conflicting information between the title of the accession and the description. All this should make you want to check your results carefully. 

If you know the clade you are working with, look at the tree carefully and see if there are some weird relationships. If you don't know the clade well, you can look for tips on very long branches, which is usually a sign that something weird is going on. If you find some of these, go back to the alignment file and see if these taxa are misaligned. It might be an error of the alignment program, the sequence might be reverse complemented, or the taxonomy doesn't match the genetics. If unsure, delete the offending sequences. Also, try analyzing the sequences with and without a constraint. Maybe the constraint is causing the problem. 