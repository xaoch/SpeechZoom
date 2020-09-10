from optparse import OptionParser
import sys

import kw_extraction_functions


### options ###

parser = OptionParser()
# filename
parser.add_option("-f", "--file", dest="filename", default="meeting_enhanced.txt",
                  help="Name of the transcript file from which to extract keywords.", metavar="FILE")
# data_dir
parser.add_option("-d", "--data_dir", dest="data_dir", default="./transcripts",
                  help="Path to the folder where to find the file.", metavar="DATA_DIR")
# results_dir
parser.add_option("-r", "--results_dir", dest="results_dir", default="./results_kw_extractions",
                  help="Path to the folder where to save the results to.", metavar="RESULTS_DIR")
# method
parser.add_option("-m", "--method", dest="method", default="rake",
                  help="The method to use for keyword extraction ('rake', 'embedrank' or 'sifrank').", metavar="METHOD")
# nb_phrases
parser.add_option("-n", "--nb_phrases", dest="nb_phrases", default="10",
                  help="Number of phrases to detect.", metavar="NB_PHRASES")
# split_size
parser.add_option("-s", "--split_size", dest="split_size", default="-1",
                  help="Number of sentences in each split (-1 == no split)", metavar="SPLIT_SIZE")
# max_length
parser.add_option("-l", "--max_length", dest="max_length", default="3",
                  help="Max number of words in the keyphrases in output. (only for the 'rake' method)", metavar="MAX_LENGTH")
(options, args) = parser.parse_args()


### keywords extraction ###

if options.method == "rake":
	kw_extraction_functions.rake_method(options.filename, data_dir=options.data_dir, results_dir=options.results_dir,
		max_length=int(options.max_length), nb_phrases=int(options.nb_phrases), split_size=int(options.split_size))

elif options.method == "embedrank":
	sys.path.append(sys.path[0]+"/embedrank")
	kw_extraction_functions.embedrank_method(options.filename, data_dir=options.data_dir, results_dir=options.results_dir,
		nb_phrases=int(options.nb_phrases), split_size=int(options.split_size))

elif options.method == "sifrank":
	sys.path.append(sys.path[0]+"/sifrank")
	kw_extraction_functions.sifrank_method(options.filename, data_dir=options.data_dir, results_dir=options.results_dir,
		nb_phrases=int(options.nb_phrases), split_size=int(options.split_size))

else:
	print("ERROR:", options.method, "method not recognized.")


