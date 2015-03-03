# last updated 2015-02-27 toby
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from itertools import islice

def get_text_to_cuis():
	"""
	Returns a dictionary of text to CUI mappings.
	"""
	text_to_cuis = dict()
	loc = "/home/toby/global_util/semmeddb/data/"
	for line in islice(read_file("text_to_cuis.txt", loc), 1, None):
		vals = line.split('|')

		text = vals[0]
		cuis = vals[1: ]
		text_to_cuis[text] = set(cuis)

	return text_to_cuis
