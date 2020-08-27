from optparse import OptionParser

import transcription_functions


### options ###
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="two_seconds_recording.wav",
                  help="Name of the audio file to be transcribed.", metavar="FILE")
parser.add_option("-n", "--nb_speakers", dest="nb_speakers", default="1",
                  help="Number of speakers in the recording.", metavar="NB_SPEAKERS")
parser.add_option("-m", "--model", dest="model", default="phone_call",
                  help="The model to use for the transcription. ('none' for standard model)", metavar="MODEL")
parser.add_option("-e", "--enhanced", dest="use_enhanced", default="false",
                  help="Wether to use an enhanced model (extra cost) or not. ('true' or 'false')", metavar="ENHANCED")

(options, args) = parser.parse_args()


data_folder_path = "./data"

if options.nb_speakers:
	nb_speakers = int(options.nb_speakers)
else:
	nb_speakers = 3

if options.use_enhanced == "True" or options.use_enhanced == "true":
	use_enhanced = True
else:
	use_enhanced = False

### transcription ###
transcription_functions.sample_long_running_recognize(filename=options.filename, data_folder_path=data_folder_path,
	model=options.model, diarization_speaker_count=nb_speakers, use_enhanced=use_enhanced)



