from optparse import OptionParser

import transcription_functions


### options ###
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="two_seconds_recording.wav",
                  help="Name of the audio file to be transcribed.", metavar="FILE")
parser.add_option("-n", "--nb_speakers", dest="nb_speakers", default="1",
                  help="Number of speakers in the recording.", metavar="NB_SPEAKERS")
parser.add_option("-m", "--model", dest="model", default="phone_call",
                  help="The model to use for the transcription.", metavar="MODEL")

(options, args) = parser.parse_args()


### transcription ###
transcription_functions.sample_long_running_recognize(filename=options.filename, model=options.model, 
	diarization_speaker_count=int(options.nb_speakers))
