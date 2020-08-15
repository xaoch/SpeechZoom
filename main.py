import sys
import transcribe


# parameters
if len(sys.argv) > 1:
	filename = sys.argv[1]
else:
	filename = "two_seconds_recording.wav"

if len(sys.argv) > 2:
	diarization_speaker_count = int(sys.argv[2])
else:
	diarization_speaker_count = 1

if len(sys.argv) > 3:
	model = sys.argv[3]
else:
	model = "phone_call"


# transcription
transcribe.sample_long_running_recognize(filename=filename, model=model,
	diarization_speaker_count=diarization_speaker_count)
