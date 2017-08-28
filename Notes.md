# Fungi Tree of Life

## Fungal clades that didn't work

Zoopagomycotina: didn't work after "good_clusters". Had 99 before that.
Nephridiophagidae: only 2two sequences after good clusters.

Cryptomycota: no data
Neocallimastigales_29006: no data

## Notes
In Agaricomycotina_5302, the taxon name CIMAP:Gly082010 needs to be fixed by removing the colon. This clade (subphyllum) finished but I'm going to break it into smaller clades to make sure it's ok.

If you brake a big clade, how do you include samples labeled as "environmental", "unclassified", and "incertae sedis"?

In Agaricomycetes_155619, the taxon name CIMAP:Gly082010 needs to be fixed by removing the colon.
	There is a clade of 27 taxa on a long branch but it's because they have one locus that no one else has
	
## Notes and Fixes
* Agaricomycetes_155619: 27 taxa deleted manually (no overlap)
* Tremellomycetes_155616: 10 taxa deleted
* Mucoromycotina_451507: 1 taxon deleted
* Arthoniomycetes_147539: 4 taxa deleted
* Leotiomycetes_147548: 4 taxa deleted
* Orbiliomycetes_189478: 2 taxa deleted
* Pezizomycetes_147549: 5 taxa deleted
* 


### Revcomp experiments
* Ustilaginomycotina_452284: did revcomp in align_tip_clusters.py and got 1068 sequences instead of 465 without revcomp. Many duplicates.   
	* Removed duplicates in Geneious and ran RAxML without partitions.
	* Tree looks very similar
* Tremellomycetes_155616: same as above. From 375 to 677 with duplicates.
	* Removed duplicates in Geneious and ran RAxML without partitions.
	* Tree looks very a bit better. Only delete two taxa
* Pucciniomycotina_29000: got more sequences (917 from 569) and a longer alignment (from ~9600 to ~11600), but with no duplicates. 