# last updated 2015-02-27 toby
"""
Maps each snippet of text to all of the CUIs it could represent.
"""

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from collections import defaultdict
from itertools import islice

print "Reading data"
text_to_cui = defaultdict(set)
for line in islice(read_file("data/pred_concept_source_text.txt"), 1, None):
	pid, sid, sub, obj, sub_text, obj_text = line.split('\t')
#	some text fields are empty, probably due to errors, so are ignored

	assert "|" not in sub_text, "| in {0}".format(sub_text)
	assert "|" not in obj_text, "| in {0}".format(obj_text)

	if sub_text:
		s_cuis = sub.split('|')
		text_to_cui[sub_text] |= set(s_cuis)

	if obj_text:
		o_cuis = obj.split('|')
		text_to_cui[obj_text] |= set(o_cuis)

print "Writing to file"
with open("./data/text_to_cuis.txt", "w") as out:
	out.write("text|cuis\n")
	for text, cuis in sorted(text_to_cui.items()):
		out.write("{0}|{1}\n".format(text, "|".join(cuis)))
