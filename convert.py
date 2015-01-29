# last updated 2015-01-28 toby

# uses NCBI's eutils api to convert
# disease mims to concept unique identifiers (CUIs)
# and the reverse (CUI -> dmim)

# UID stands for MedGen unique identifier
# mim is OMIM identifier
# NCBI = National Center for Biotechnology Information

import json
import logging
import re
import sys
import urllib2

def query_ncbi(url):
	BASE = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	response = urllib2.urlopen(BASE + url)
	return response.read()

#-------------------------------------------------------------------------------

def uid_to_cui(uid): # one uid to one cui
	req = "esummary.fcgi?db=medgen&id=" + uid
	xml = query_ncbi(req)

	if re.search(r'cannot get document summary', xml) is not None:
		logging.warning("UID {0} does not exist!".format(uid))
		return ""

	res = re.findall(r'<ConceptId>C\w\d{6}</ConceptId>', xml)
	assert len(res) == 1, "More than one CUI for UID {0}".format(uid)
	return res[0][11:-12]

def cui_to_uid(cui): # one cui to one uid
	req = "esearch.fcgi?db=medgen&term=" + cui + "[conceptid]"
	xml = query_ncbi(req)

	if re.search(r'No items found.', xml) is not None:
		logging.warning("No UID exists for {0}".format(cui))
		return ""

	res = re.findall(r'<Id>\d+</Id>', xml)
	assert len(res) == 1, "More than one UID for {0}".format(cui)
	return res[0][4:-5]

#-------------------------------------------------------------------------------

def uid_to_dmim(uid): # one uid to many dmim
	req = "esummary.fcgi?db=medgen&id=" + uid
	xml = query_ncbi(req)

	if re.search(r'cannot get document summary', xml) is not None:
		logging.warning("UID {0} does not exist!".format(uid))
		return []

	res = re.findall(r'&lt;MIM&gt;\d{6}&lt;/MIM&gt;', xml)
	return set([dmim[11:-12] for dmim in res])

def dmim_to_uid(dmim): # one dmim to many uid
	req = "esearch.fcgi?db=medgen&term=" + dmim + "[mim]"
	xml = query_ncbi(req)

	if re.search(r'No items found.', xml) is not None:
		logging.warning("DMIM {0} does not exist in MedGen.".format(dmim))
		return []

	res = re.findall(r'<Id>\d+</Id>', xml)
	return set([uid[4:-5] for uid in res])

#-------------------------------------------------------------------------------

def dmim_to_cui(dmim):
#	one dmim to many cui
#	returns CUIs starting with CN...

	uids = dmim_to_uid(dmim)
	if not uids:
		return []

	return map(uid_to_cui, uids)

def cui_to_dmim(cui):
#	one cui to many dmim
#	gives empty list if cui and uid exist but no dmim exists

	uid = cui_to_uid(cui)
	return uid_to_dmim(uid)

#-------------------------------------------------------------------------------

def geneID_to_gmim(gene_id):
#	one entrez gene id to one omim gene id (hopefully..)
#	gives the (hopefully unique) gmim of a entrez geneid

	req = "esummary.fcgi?db=gene&id=" + gene_id + "&retmode=json"
	resp = query_ncbi(req)

	tree = json.loads(resp)

#	prob gonna have errors at this line
	gmims = tree["result"][gene_id]["mim"]

	assert len(gmims) == 1, "too many gmims {0}".format(gene_id)
	return gmims[0]



def gmim_to_geneID(gmim):
#	gmim 603072 gives 6790 and 8465 but 8465 is deprecated

#	TODO TODO TODO TODO TODO TODO TODO
#	should only return one string!!!


#	converts a gene MIM into a gene ID (should be 1 to 1)
#	returns only the current identifier
#	remove the current only filter and it returns deprecated identifiers
#	which may be necessary since the databases are pretty old..

#	but it seems that both semmeddb and implicitome use current identifiers
	req = "esearch.fcgi?db=gene&term=" + gmim + "[mim]+AND+current+only[filter]"
	xml = query_ncbi(req)

	if (re.search(r'No items found.', xml) is not None
		or re.search(r'<Count>0</Count>', xml) is not None):
		print "Gene MIM {0} has no gene ID.".format(gmim)
		return ""

	res = re.findall(r'<Id>\d+</Id>', xml)

	if len(res) == 1:
		return res[0][4:-5]

#	multiple... so backconvert and cross check
	gene_ids = [gid[4:-5] for gid in res]

	temp_gmims = map(geneID_to_gmim, gene_ids)
	assert temp_gmims.count(gmim) == 1, "too many gmimsasdfasdf {0}".format(gmim)
	return gene_ids[temp_gmims.index(gmim)]


def main():
	print gmim_to_geneID("603175")
if __name__ == "__main__":
	main()
