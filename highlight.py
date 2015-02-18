# last updated 2015-02-18 toby

# given a specific sentence and predication id
# we want to highlight the sub, pred, obj in the sentence with html tags

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

import mysql.connector
import DB_LOGINS as DB

from semmed_info import get_sentence
from collections import namedtuple

Location = namedtuple("Location", "start stop")

def separate(a, b):
	assert a.start < a.stop and b.start < b.stop
	return b.start > a.stop or a.start > b.stop

def check(sub, pred, obj):
	return separate(sub, pred) and separate(pred, obj) and separate(sub, obj)

def add_tag(tag, text):
	return "<span class=\"{0}\">{1}</span>".format(tag, text)

def find_locations(pred_id, sent_id):
	cnx = mysql.connector.connect(database = "semmeddb", **DB.SENTINEL)
	if cnx.is_connected():
		cur = cnx.cursor()

#		some predications are extracted multiple times from the same
#		sentence (eg sid 122884583, pid 539853). this predication is
#		extracted 1, 2, and 3 times from one sentence
#		since i do not care about how many times the predication was
#		extracted from the sentence, I only want one of the multiple
#		proofs, if they do exist. hence the "limit 1"
		query = ("SELECT SUBJECT_START_INDEX, SUBJECT_END_INDEX, "
			"PREDICATE_START_INDEX, PREDICATE_END_INDEX, "
			"OBJECT_START_INDEX, OBJECT_END_INDEX "
			"FROM SENTENCE_PREDICATION "
			"WHERE SENTENCE_ID = %s AND PREDICATION_ID = %s LIMIT 1;")

		cur.execute(query, (sent_id, pred_id))
		res = cur.fetchone()
		assert len(res) == 6

		cur.close()
	cnx.close()

	res = map(lambda x: x-1, res)
	sub = Location(res[0], res[1])
	pred = Location(res[2], res[3])
	obj = Location(res[4], res[5])
	return (sub, pred, obj)

#def highlight(sentence, sub, pred, obj):
#	print sentence
#
#	t = ["."] * len(sentence)
#	t[sub.start] = 's'
#	t[sub.stop] = 'S'
#
#	t[pred.start] = 'p'
#	t[pred.stop] = 'P'
#	t[obj.start] = 'o'
#	t[obj.stop] = 'O'
#
#	print "".join(t)
#	return
#
#
#
#
#
#	for i, v in enumerate(sentence):
#		if i in locations:
#			sys.stdout.write("*")
#		else:
#			sys.stdout.write(".")
#
#	sys.stdout.write("\n")

#def work(sentence, sub, pred, obj):
##	put tags around
#	assert check(sub, pred, obj)
#
#	print sub, pred, obj
#
#	starts = sorted([0, sub.start, pred.start, obj.start, sub.stop+1, pred.stop+1, obj.stop+1])
#	stops = sorted([sub.stop+1, pred.stop+1, obj.stop+1, sub.start, pred.start, obj.start, len(sentence)])
#
#	print starts
#	print stops
#
#
#	sub_text = sentence[sub.start : sub.stop+1]
#	pred_text = sentence[pred.start : pred.stop+1]
#	obj_text = sentence[obj.start : obj.stop+1]
#
#	ans = ""
#	for a, b in zip(starts, stops):
#		fragment = sentence[a:b]
#
#		if fragment == sub_text:
#			ans += add_tag("subject", sub_text)
#		elif fragment == obj_text:
#			ans += add_tag("object", obj_text)
#		elif fragment == pred_text:
#			ans += add_tag("predicate", pred_text)
#		else:
#			ans += fragment
#
#		print a, b
#		print "---{0}---".format(sentence[a:b])
#
#	print "------------------------"
#
#	print ans
#	print "************************"


def highlight(sentence, sub, pred, obj):
#	given the sentence and the positions of the subject, object, and predicate
#	return a string with the html tags inserted
	starts = sorted([0, sub.start, pred.start, obj.start, sub.stop+1, pred.stop+1, obj.stop+1])
	stops = sorted([sub.stop+1, pred.stop+1, obj.stop+1, sub.start, pred.start, obj.start, len(sentence)])

	text = dict()
	text[sentence[sub.start : sub.stop+1]] = "subject"
	text[sentence[obj.start : obj.stop+1]] = "object"
	text[sentence[pred.start : pred.stop+1]] = "predicate"

	ans = ""
	for a, b in zip(starts, stops):
		fragment = sentence[a:b]
		if fragment in text:
			ans += add_tag(text[fragment], fragment)
		else:
			ans += fragment

	return add_tag("sentence", ans)

def main():
	for line in read_file("a.txt"):
		pid, sid = line.split('|')
		sub, pred, obj = find_locations(pid, sid)
		sent = get_sentence(sid)

		print highlight(sent, sub, pred, obj)
#		work(sent, sub, pred, obj)
		raw_input("Press Enter to continue...")

	return


	print "hi"
	pid = "539852"
	sid = "3666031"
	a = find_locations(pid, sid)
	b = get_sentence(sid)

	print b
	print a
	highlight(b, a)


if __name__ == "__main__":
	main()
