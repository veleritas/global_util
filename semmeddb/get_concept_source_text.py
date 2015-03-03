# last updated 2015-02-28 toby
"""
Returns the text snippets that the subject and object text came from.
"""
import sys
sys.path.append("/home/toby/global_util/")
from query_semmed import query_semmed

def get_concept_source_text(sentence_id, predication_id):
	"""
	Returns subject_text, object_text.
	"""
	query = ("SELECT SUBJECT_TEXT, OBJECT_TEXT "
		"FROM SENTENCE_PREDICATION "
		"WHERE SENTENCE_ID = %s "
		"AND PREDICATION_ID = %s LIMIT 1;")
	vals = (sentence_id, predication_id)

	sub_text = "NO_RESPONSE" # if there are no rows
	obj_text = "NO_RESPONSE"
	for row in query_semmed(query, vals):
		sub_text = row[0]
		obj_text = row[1]

	return (sub_text, obj_text)
