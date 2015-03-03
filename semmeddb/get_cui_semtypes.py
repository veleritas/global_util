# last updated 2015-02-27 toby
"""
Returns the semantic types of all CUIs in SemMedDB.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from itertools import islice

def get_cui_semtypes():
	"""
	Returns the unique semantic types of a CUI as a dict of set.
	"""
	cui_semtypes = dict()
	loc = "/home/toby/global_util/semmeddb/data/"
	for line in islice(read_file("cui_semtypes.txt", loc), 1, None):
		vals = line.split('|')
		cui = vals[0]
		semtypes = vals[1: ]

		cui_semtypes[cui] = set(semtypes)

	return cui_semtypes
