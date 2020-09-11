from optparse import OptionParser

import transcription_functions


### options ###

parser = OptionParser()
# filename
parser.add_option("-f", "--file", dest="filename", default="two_seconds_recording.wav",
                  help="Name of the audio file to be transcribed.", metavar="FILE")
# data directory
parser.add_option("-d", "--data_dir", dest="data_dir", default="./data",
                  help="Path to the folder where to find the file.", metavar="DATA_DIR")
# transcript directory
parser.add_option("-t", "--transcript_dir", dest="transcript_dir", default="./transcripts",
                  help="Path to the folder where to save the transcript.", metavar="TRANSCRIPT_DIR")
# confidences directory
parser.add_option("-c", "--confidences_dir", dest="confidences_dir", default="./confidences",
                  help="Path to the folder where to save confidences results.", metavar="CONFIDENCES_DIR")
# number of speakers
parser.add_option("-n", "--nb_speakers", dest="nb_speakers", default="1",
                  help="Number of speakers in the recording.", metavar="NB_SPEAKERS")
# model (for the transcription)
parser.add_option("-m", "--model", dest="model", default="phone_call",
                  help="The model to use for the transcription ('command_and_search', 'phone_call', 'video' or 'none'. Note that 'none' refers to the standard model).", metavar="MODEL")
# use enhanced model or not
parser.add_option("-e", "--enhanced", dest="use_enhanced", default="true",
                  help="Whether to use an enhanced model (extra cost) or not. ('true' or 'false')", metavar="ENHANCED")
(options, args) = parser.parse_args()

# convert string to boolean
if options.use_enhanced == "True" or options.use_enhanced == "true":
	use_enhanced = True
else:
	use_enhanced = False

### transcription ###

transcription_functions.sample_long_running_recognize(filename=options.filename, data_dir=options.data_dir,
	transcript_dir=options.transcript_dir, confidences_dir=options.confidences_dir, enable_speaker_diarization=True,
	nb_speakers=int(options.nb_speakers), model=options.model, enable_word_confidence=True, use_enhanced=use_enhanced)



