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
``python extract_keywords.py --file=... --data_dir=... --results_dir=... --method=... --nb_phrases=... --split_size=... --max_length=...``

options:
--file: Name of the transcript file from which to extract keywords. (default: meeting_enhanced.txt)
--data_dir: Path to the folder where to find the file. (default: ./transcripts)
--results_dir: Path to the folder where to save the results to. (default: ./results_kw_extractions)
--method: The method to use for keyword extraction ('rake', 'embedrank' or 'sifrank'). (default: rake)
--nb_phrases: Number of phrases to detect. (default: 10)
--split_size: Number of sentences in each split (-1 == no split). (default: -1)
--max_length: Max number of words in the keyphrases in output.(only for the 'rake' method) (default: 3)