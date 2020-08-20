import re


def preprocess_dialogue(string_text):
	preprocessing = re.sub(r"\n\[[0-9]\]\n", "", string_text)
	return preprocessing


def rake_method(filename, data_folder_path="./transcripts"):
	from rake_nltk import Rake

	transcript_path = data_folder_path + "/" + filename
	with open(transcript_path, 'r') as transcript_file:
		transcript = transcript_file.read()
	preprocessed_transcript = preprocess_dialogue(transcript)

	# rake method
	r = Rake()
	r.extract_keywords_from_text(preprocessed_transcript)
	ranked_phrases = r.get_ranked_phrases()

	print("ranked phrases:")
	print(ranked_phrases)

	return ranked_phrases


def swisscom_method(filename, data_folder_path="./transcripts", nb_phrases=10):
	import launch

	transcript_path = data_folder_path + "/" + filename
	with open(transcript_path, 'r') as transcript_file:
		transcript = transcript_file.read()
	preprocessed_transcript = preprocess_dialogue(transcript)

	# swisscom method
	embedding_distributor = launch.load_local_embedding_distributor()
	pos_tagger = launch.load_local_corenlp_pos_tagger()

	kp = launch.extract_keyphrases(embedding_distributor, pos_tagger, preprocessed_transcript, nb_phrases, 'en')

	print("ranked phrases:")
	print(kp)

	return kp