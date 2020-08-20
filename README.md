#Installation

Follow installation steps in "INSTALLATIONS.md"


#Usage

##Speech-to-text recognition

command:
``python transcribe.py --file=... --nb_speakers=... --model=...``

options:
--file: Name of the audio file to transcribe. (default: two_seconds_recording.wav)
--nb_speakers: Number of speakers in the recording. (default: 1)
--model: The model to use for the transcription.. (default: phone_call)


##Keywords detection

command:
``python extract_keywords.py --file=... --method=...``

options:
--file: Name of the transcript file from which to extract keywords. (default: transcript_3_people_recording.txt)
--method: Number of speakers in the recording. (default: rake)