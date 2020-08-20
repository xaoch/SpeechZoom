from optparse import OptionParser
import sys

import kw_extraction_functions

transcripts_path = "./transcripts"

### options ###
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="transcript_3_people_recording.txt",
                  help="Name of the transcript file from which to extract keywords.", metavar="FILE")
parser.add_option("-m", "--method", dest="method", default="rake",
                  help="The method to use for keyword extraction (rake or swisscom).", metavar="METHOD")

(options, args) = parser.parse_args()

if options.method == "rake":
	kw_extraction_functions.rake_method(options.filename, data_folder_path=transcripts_path)

elif options.method == "swisscom":
	sys.path.append(sys.path[0]+"/swisscom")
	nb_phrases=10
	kw_extraction_functions.swisscom_method(options.filename, data_folder_path=transcripts_path, nb_phrases=nb_phrases)