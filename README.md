# ARM (Association Rule Mining) Project
Implemented Apriori and FP growth algorithms with optimisations.
## FP Growth
Implemented the FP Growth algorithm to generate closed frequent itemsets at runtime with the merging strategy optimisation as : push right the branches that have been mined for a particular item say p, i.e. push these branches to the remaining branch(es)of the FP-tree as it can be time and space consuming to generate numerous conditional pattern bases.
## Apriori
Implemented the Apriori algorithm to generate closed frequent itemsets at runtime using two optimisations strategies: Hash-based technique and Partitioning.
### Hash-based Technique
When scanning each transaction in the database to generate the frequent 1-itemsets , we can generate all the 2-itemsets for each transaction, hash (i.e., map) them into the different buckets of a hash table structure, and increase the corresponding bucket counts. A 2-itemset with a corresponding bucket count in the hash table that is below the support threshold cannot be frequent and thus is removed from the candidate set.
### Partitioning Technique
Distributed and Parallel algorithms for apriori based frequent itemset mining obey a rule : If the database D is divided into n partitions and frequent itemset mining is performed in each of them individually, any itemset that is potentially frequent with respect to D must occur as a frequent itemset in at least one of those n partitions. Now the algorithm can be on each of those partitions in parallel and all the local frequent itemsets generated can be checked for being globally frequent by a scan of the database again.
## Project Report
[Link](https://docs.google.com/document/d/1sW-F1rnOsA1R3j3pCe7N_H_vIa3B_0AkkEfuX3DPjgc/edit?usp=sharing)
