import re
import datetime
import os
import json



def preprocess_dialogue(text):
	"""Preprocess a dialogue text to make it ready for the keywords extraction functions.
	
	Remove square brackets and add ellipses at the end of incomplete sentences.

	Parameters
	----------
	text : str
		Text to be preprocessed.

	Returns
	-------
	str
		Preprocessed text (square brackets removed and ellipses add at the end of incomplete sentences).
	
	"""
	preprocessing = re.sub(r"\.\s\n\[[0-9]\]\n", ". ", text)
	preprocessing = re.sub(r"\,\s\n\[[0-9]\]\n", "... ", preprocessing)
	preprocessing = re.sub(r"\?\s\n\[[0-9]\]\n", "? ", preprocessing)
	preprocessing = re.sub(r"\.\n\[[0-9]\]\n", ". ", preprocessing)
	preprocessing = re.sub(r"\?\n\[[0-9]\]\n", "? ", preprocessing)
	preprocessing = re.sub(r"\s\n\[[0-9]\]\n", "... ", preprocessing)
	preprocessing = re.sub(r"\n\[[0-9]\]\n", "...", preprocessing)
	preprocessing = re.sub(r"\[[0-9]\]\n", "", preprocessing)
	preprocessing = re.sub(r"\n", "", preprocessing)

	return preprocessing



def split_text(text, split_size=-1):
	"""Preprocess a dialogue text to make it ready for the keywords extraction functions.
	
	Remove square brackets and add ellipses at the end of incomplete sentences.

	Parameters
	----------
	text : str
		Text to split.
	split_size : int
		Required size of each part of the text (in number of sentences). (if -1 =>  no split)

	Returns
	-------
	list
		List of the parts of the text

	"""

	if split_size == -1:
		return [text]
	else:
		iter_points = re.finditer(r"(\.)+", text)
		iter_question_marks = re.finditer(r"\?", text)
		indices = [m.start(0) for m in iter_points] + [m.start(0) for m in iter_question_marks]
		indices.sort()
		nb_sentences = len(indices)
		print("Split size =", split_size, ";", nb_sentences, "sentences found. Splitting the text into", nb_sentences//split_size, "parts.")
		
		text_parts = []
		previous_idx = 0
		current_idx = split_size - 1
		while current_idx < nb_sentences:
			text_parts.append(text[previous_idx:indices[current_idx]+1])
			previous_idx = indices[current_idx] + 1
			current_idx += split_size
		
		if current_idx>nb_sentences and current_idx<nb_sentences+split_size:
			text_parts[-1]+=text[previous_idx:]

		return text_parts



def load_text(filename, data_dir="./transcripts"):

	transcript_path = data_dir + "/" + filename
	with open(transcript_path, 'r') as transcript_file:
		transcript = transcript_file.read()
	return transcript



def save_results(text_parts, keywords_per_part, scores_per_part, infos_dict, results_dir="./results_kw_extractions"):
	"""Save the results of the keywords extraction.
	
	The results are saved in a new folder with 3 documents inside: one for the keywords, one for the scores, one for the parameters.
	
	Parameters
	----------
	text_parts : list
		list of the parts of the text
	keywords_per_part : list
		list of the keywords corresponding to each part of the text
	scores_per_part : list
		list of the keywords-scores corresponding to each part of the text
	infos_dict : dict
		dictionnary containing some information on the parameters of the test
	results_dir : str
		relative path to the drectory where all results on keywords extraction are saved
	
	"""

	# create subfolder for this text
	text_dir = results_dir + "/" + infos_dict["text_name"]
	kw_subfolders = [f.name for f in os.scandir(results_dir) if f.is_dir() ]
	if not infos_dict["text_name"] in kw_subfolders:
		os.makedirs(text_dir)

	# create subfolder for this method
	method_dir = text_dir + "/" + infos_dict["method"]
	text_subfolders = [f.name for f in os.scandir(text_dir) if f.is_dir() ]
	if not infos_dict["method"] in text_subfolders:
		os.makedirs(method_dir)

	# date
	date = str(datetime.datetime.now())
	date = date.replace(" ", "_")
	date = date.replace(":", "-")
	date = date.split(".", 1)[0]
	
	# create a folder for this test (named after to the date of the test)
	new_test_dir = method_dir + "/" + date
	os.makedirs(new_test_dir)

	# save infos (parameters of the test) in new file
	infos = ""
	for key in list(infos_dict.keys()):
		infos += key + ": " + infos_dict[key] + "\n"
	with open(new_test_dir + "/infos.txt", "w") as infos_file:
		infos_file.write(infos)

	# save keywords in new file
	test = ""
	for i in range(len(text_parts)):
		test += "### PART " + str(i) + " ###\n\n"
		test += "Text:\n"
		test += text_parts[i] + "\n\n"
		test += "Keywords:\n"
		test += str(keywords_per_part[i]) + "\n\n\n"
	with open(new_test_dir + "/keywords.txt", "w") as kw_file:
		kw_file.write(test)

	# save scores in nnew file
	with open(new_test_dir+"/scores.json", "w") as json_file:
		json_file.write(json.dumps(scores_per_part))











