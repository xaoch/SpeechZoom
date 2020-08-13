import sys
import transcribe


if len(sys.argv) > 1:
	filename = sys.argv[1]
else:
	filename = "two_seconds_recording.wav"


if len(sys.argv) > 2:
	model = sys.argv[2]
else:
	model = "phone_call"

transcribe.sample_long_running_recognize(filename=filename, model=model)
