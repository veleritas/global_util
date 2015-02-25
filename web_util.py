# last updated 2015-02-24 toby

def add_tag(tag_name, tag_class, text, tag_id = "", display = ""):
	return "<{0} class=\"{1}\" id=\"{3}\" style=\"display: {4}\">{2}</{0}>".format(tag_name, tag_class, text, tag_id, display)
