# last updated 2015-01-26 toby
import re

def is_cui(cui):
	return re.match(r'^C\w\d{6}$', cui) is not None

def is_mim(mim):
	return re.match(r'^\d{6}$', mim) is not None
