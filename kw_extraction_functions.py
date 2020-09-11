import utils


def rake_method(filename, data_dir="./transcripts", results_dir="./results_kw_extractions", max_length=3, nb_phrases=10, split_size=-1):
	"""Apply Rake algorithm on the text of the given file, then save results.
	
	Parameters
	----------
	filename : str
		Name of the file from which the text is loaded.
	data_dir : str
		Path of the folder where to find the file 'filename'.
	results_dir : str
		Path of the folder where to save results.
	max_length : int
		Max number of words in the keyphrases in output.
	nb_phrases : int
		Number of keyphrases to select in each part of the text.
	split_size : int
		Required size of each part of the text (in number of sentences). (if -1 =>  no split)

	"""
	from rake_nltk import Rake
	import nltk

	# preprocess data
	text = utils.load_text(filename, data_dir=data_dir)
	preprocessed_dialogue = utils.preprocess_dialogue(text)
	splitted_dialogue = utils.split_text(preprocessed_dialogue, split_size)

	# set stopwords
	stopwords = nltk.corpus.stopwords.words("english")
	extra_stopwords = ["..."]
	stopwords = stopwords+extra_stopwords
	
	# initialize rake
	r = Rake(stopwords=stopwords, max_length=max_length)

	# apply Rake on each part of the text
	keyphrases_per_part = []
	scores_per_part = []
	for idx in range(len(splitted_dialogue)):
		print("\n########### PART ", idx, "###########")
		text_portion = splitted_dialogue[idx]
		r.extract_keywords_from_text(text_portion)
		ranked_phrases = r.get_ranked_phrases()
		ranked_scores = r.get_ranked_phrases_with_scores()
		truncated_phrases = ranked_phrases[:min(len(ranked_phrases),nb_phrases)]
		truncated_scores = ranked_scores[:min(len(ranked_scores),nb_phrases)]
		print(truncated_phrases)
		keyphrases_per_part.append(truncated_phrases.copy())
		scores_per_part.append([(truncated_scores[i][1],truncated_scores[i][0]) for i in range(len(truncated_scores))])

	# save results
	method="rake"
	infos = {"method":method, "text_name": filename.split(".")[0], "split_size":str(split_size), "nb_phrases":str(nb_phrases)}
	utils.save_results(splitted_dialogue, keyphrases_per_part, scores_per_part, infos, results_dir=results_dir)



def embedrank_method(filename, data_dir="./transcripts", results_dir="./results_kw_extractions", nb_phrases=10, split_size=-1):
	"""Apply EmbedRank algorithm on the text of the given file, then save results.
	
	Link to the paper: https://arxiv.org/abs/1801.04470
	Link to the Github: https://github.com/swisscom/ai-research-keyphrase-extraction
	
	Parameters
	----------
	filename : str
		Name of the file from which the text is loaded.
	data_dir : str
		Path of the folder where to find the file 'filename'.
	results_dir : str
		Path of the folder where to save results.
	nb_phrases : int
		Number of keyphrases to select in each part of the text.
	split_size : int
		Required size of each part of the text (in number of sentences). (if -1 =>  no split)

	"""
	import launch

	# preprocess data
	text = utils.load_text(filename, data_dir=data_dir)
	preprocessed_dialogue = utils.preprocess_dialogue(text)
	splitted_dialogue = utils.split_text(preprocessed_dialogue, split_size)

	# initialize embedding distributor and POS tagger
	embedding_distributor = launch.load_local_embedding_distributor()
	pos_tagger = launch.load_local_corenlp_pos_tagger()

	# apply EmbedRank on each part of the text
	keyphrases_per_part = []
	scores_per_part = []
	for idx in range(len(splitted_dialogue)):
		print("\n########### PART ", idx, "###########")
		text_portion = splitted_dialogue[idx]
		kp = launch.extract_keyphrases(embedding_distributor, pos_tagger, text_portion, nb_phrases, 'en')
		print(kp[0])
		keyphrases_per_part.append(kp[0].copy())
		scores_per_part.append([(kp[0][i], kp[1][i]) for i in range(len(kp[0]))])
	
	# save results
	method = "embedrank"
	infos = {"method":method, "text_name": filename.split(".")[0], "split_size":str(split_size), "nb_phrases":str(nb_phrases)}
	utils.save_results(splitted_dialogue, keyphrases_per_part, scores_per_part, infos, results_dir=results_dir)



def sifrank_method(filename, data_dir="./transcripts", results_dir="./results_kw_extractions", nb_phrases=10, split_size=-1, sifrank_plus=True, cuda_device=-1):
	"""Apply SIFRank algorithm on the text from the given file, then save results.

	Link to the paper: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8954611
	Link to the Github: https://github.com/sunyilgdx/SIFRank
	
	Parameters
	----------
	filename : str
		Name of the file from which the text is loaded.
	data_dir : str
		Path to the folder where to find the file 'filename'.
	results_dir : str
		Path to the folder where to save results.
	nb_phrases : int
		Number of keyphrases to select in each part of the text.
	split_size : int
		Required size of each part of the text (in number of sentences). (-1 =>  no split)
	sifrank_plus : bool
		Whether to use SIFRank_plus or not
	cuda_device : int
		The GPU device to run on (-1 => no GPU).

	"""
	import nltk
	from embeddings import sent_emb_sif, word_emb_elmo
	from model.method import SIFRank, SIFRank_plus
	from stanfordcorenlp import StanfordCoreNLP

	# preprocess data
	text = utils.load_text(filename, data_dir=data_dir)
	preprocessed_dialogue = utils.preprocess_dialogue(text)
	splitted_dialogue = utils.split_text(preprocessed_dialogue, split_size)

	# settings for SIFRank
	options_file = "./sifrank/auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_options.json"
	weight_file = "./sifrank/auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_5.5B_weights.hdf5"
	porter = nltk.PorterStemmer()
	ELMO = word_emb_elmo.WordEmbeddings(options_file, weight_file, cuda_device=-1)
	SIF = sent_emb_sif.SentEmbeddings(ELMO, lamda=1.0,
		weightfile_pretrain='./sifrank/auxiliary_data/enwiki_vocab_min200.txt',
		weightfile_finetune='./sifrank/auxiliary_data/inspec_vocab.txt',
		auxiliary_data_path='./sifrank/auxiliary_data')
	en_model = StanfordCoreNLP("./sifrank/stanford-corenlp-4.1.0", quiet=True)
	elmo_layers_weight = [0.0, 1.0, 0.0]

	# apply SIFRank on each part of the text
	keyphrases_per_part = []
	scores_per_part = []
	for idx in range(len(splitted_dialogue)):
		print("\n########### PART ", idx, "###########")
		text_portion = splitted_dialogue[idx]
		if sifrank_plus:
			keyphrases_scores = SIFRank_plus(text_portion, SIF, en_model, N=nb_phrases, elmo_layers_weight=elmo_layers_weight)
		else:
			keyphrases_scores = SIFRank(text_portion, SIF, en_model, N=nb_phrases, elmo_layers_weight=elmo_layers_weight)
		keyphrases = [keyphrases_scores[i][0] for i in range(len(keyphrases_scores))]
		print(keyphrases)
		keyphrases_per_part.append(keyphrases.copy())
		scores_per_part.append(keyphrases_scores.copy())

	# save results
	method = "sifrank"
	infos = {"method":method, "text_name": filename.split(".")[0], "split_size":str(split_size), "nb_phrases":str(nb_phrases)}
	utils.save_results(splitted_dialogue, keyphrases_per_part, scores_per_part, infos, results_dir=results_dir)










