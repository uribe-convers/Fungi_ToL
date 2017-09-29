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

## Combining Clades

The combined (backbone + clade tree) tree for some of these clades has less leaves that it should! This is after taking in consideration shared species. Couldn't pinpoint the problem but here are some examples:

* Dothideomycetes_147541
	* 7 taxa shared
	* Tree should have 4241 tips
	* Tree has 4235
	* Offending taxa: _Cochliobolus heterostrophus, Pleospora herbarum, Trypethelium unknown, Dendrographa minor, Roccella fuciformis, Simonyella variegata_
	* All of these are in the backbone but not in the combined tree.

* Arthoniomycetes_147539
	* 1 taxon shared
	* Tree should have 485 tips
	* Tree has 484
	* Offending taxon: _Dendrographa minor_

### Notes on Combining trees
The order in which the trees are passed to the script matters! When combining Entomophthoromycotina\_1264859 with a combined tree (Combined_6), changing the order of the input trees results in the same number of tips in the combined tree, but the tips are different!  

**I'm always picking the order that results in the largest combined tree**

Geminibasidiomycetes_1708517 doesn't have mrca and when I included outgroups it results in a combined tree of few species. This clade only has 5 species though. **Skipping**

Kickxellomycotina_451828 (23 taxa) has no mrca in the combined tree. I tried adding the complete Zygomycota_1264859 clade instead (40 taxa) but I get the following error: **Skipping**

```
new root label:Traceback (most recent call last):
  File "../../src_PyPHLAWD/combine_trees.py", line 65, in <module>  
    for i in nrt.children:  
AttributeError: 'NoneType' object has no attribute 'children'
```

Lichinomycetes_315355 (33 taxa) has no mrca. **Skipping**

Microsporidia_6029 (191 taxa) results in same number of taxa in combined tree when the order in which the trees are passed to the script is different, but the taxa are different. There is only one that is different though.

Wallemiomycetes_431957 (7 taxa) has no mrca. **Skipped**

**Skipped Sordariomycetes_147550 while it's runnig with outgroups!**