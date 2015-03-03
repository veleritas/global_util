# last updated 2015-02-28 toby
"""
Read the text snippet to concept semantic type mappings from a file and
returns the mappings as a dict of set.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from itertools import islice

def get_text_semtypes():
	text_semtypes = dict()
	loc = "/home/toby/global_util/semmeddb/data/"
	for line in islice(read_file("text_semtypes.txt", loc), 1, None):
		vals = line.split('|')
		text = vals[0]
		semtypes = vals[1: ]

		text_semtypes[text] = set(semtypes)

	return text_semtypes
