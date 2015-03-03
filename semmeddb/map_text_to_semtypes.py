# last updated 2015-02-27
"""
Generates the mapping from text snippet to semantic type. Prints result
to a text file.
"""
from get_cui_semtypes import get_cui_semtypes
from get_text_to_cuis import get_text_to_cuis
from collections import defaultdict

import logging
logging.basicConfig(filename = "map_text_to_semtypes.log",
	level = logging.DEBUG)

cui_semtypes = get_cui_semtypes()
text_to_cuis = get_text_to_cuis()

text_semtypes = defaultdict(set)
for snippet, cuis in text_to_cuis.items():
	for cui in cuis:
		if cui in cui_semtypes:
			text_semtypes[snippet] |= cui_semtypes[cui]
		else:
			logging.error("CUI {0} has no semtypes!".format(cui))

with open("./data/text_semtypes.txt", "w") as out:
	out.write("text|semtypes\n")
	for snippet, semtypes in sorted(text_semtypes.items()):
		out.write("{0}|{1}\n".format(snippet, "|".join(semtypes)))
