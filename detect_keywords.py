from rake_nltk import Rake
import pdb
import re

def preprocess_dialogue(string_text):
	preprocessing = re.sub(r"\n\[[0-9]\]\n", "", string_text)
	return preprocessing


def detect_keywords(filename, data_folder_path="./transcripts"):

	transcript_path = data_folder_path + "/" + filename
	with open(transcript_path, 'r') as transcript_file:
		transcript = transcript_file.read()
	
	preprocessed_transcript = preprocess_dialogue(transcript)

	r = Rake()
	r.extract_keywords_from_text(preprocessed_transcript)
	ranked_phrases = r.get_ranked_phrases()

	print("ranked phrases:")
	print(ranked_phrases)


filename = "transcript_3_people_recording.txt"

detect_keywords(filename, data_folder_path="./transcripts")