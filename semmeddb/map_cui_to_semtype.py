# last updated 2015-02-27 toby
"""
Prints the UMLS semantic types of each CUI into a file.

Left joining the CONCEPT table with the CONCEPT SEMTYPE table does not
seem to give all of the CUIs used by the database. For example, CUI
352997 shows up in PREDICATION_AGGREGATE (e.g. PID 3858523), but does
not exist at all in the CONCEPT table.

Therefore I also used the PREDICATION_AGGREGATE table to create find
the semtypes of a concept.
"""

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from collections import defaultdict

cui_semtypes = defaultdict(set)
for line in read_file("./data/cui_semtype.txt"):
	cui, semtype = line.split('\t')
	assert cui and semtype, "One of the fields is empty"
	cui_semtypes[cui].add(semtype)

for line in read_file("./data/pred_agg.txt"):
	vals = line.split('\t')
	assert len(vals) == 13

	sub = vals[5]
	s_type = vals[7]
	obj = vals[9]
	o_type = vals[11]

	s_cuis = sub.split('|')
	o_cuis = obj.split('|')

	for cui in s_cuis:
		cui_semtypes[cui].add(s_type)

	for cui in o_cuis:
		cui_semtypes[cui].add(o_type)

with open("./data/cui_semtypes.txt", "w") as out:
	out.write("cui|semtypes\n")
	for cui, semtypes in sorted(cui_semtypes.items()):
		out.write("{0}|{1}\n".format(cui, "|".join(semtypes)))
