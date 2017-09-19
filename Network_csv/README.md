# README #

Rewire to see whether assortativity make a difference in the occurrence of anomolous robustness.

### What is this repository for? ###

rewire FB4000,BA4000,ER4000 by means of rewiring scheme1&2

### How do I get set up? ###

rewire1.py(scheme1):network_FB4000 is original network-->FB4000_rew1.csv is adjlist of rewired network,FB4000_rew1f.csv delete the first column of FB4000_rew1.csv to be used for fortran
rewire2.py(scheme2):network_FB4000 is original network-->FB4000_rew2.csv is adjlist of rewired network,FB4000_rew2f.csv delete the first column of FB4000_rew2.csv to be used for fortran

assort.py:print assortativity of rewired networks.

only FB give birth to corelist_FB4000.csv because only FB is attacked in order of coreness.

### Contribution guidelines ###

Contributed by Qingling


### Who do I talk to? ###

Revised by Zhanglin