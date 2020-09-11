# Installation

Follow the installation steps in "INSTALLATIONS.md".


# Usage

## Speech-to-text recognition

command:
``python transcribe.py --file=<filename> --nb_speakers=<number of speakers> --model=<type of model> --enhanced=<boolean>``

options:
--file: Name of the audio file to transcribe. Default:'two_seconds_recording.wav'
--nb_speakers: Number of speakers in the recording. Default:'1'
--model: The model to use for the transcription ('command_and_search', 'phone_call', 'video' or 'none'. Note that 'none' refers to the standard model). Default:'phone_call'
--enhanced: Whether to use an enhanced model (!extra cost!) or not ('true' or 'false'). Default:'true'


## Keywords detection

command:
``python extract_keywords.py --file=<filename> --data_dir=<local path> --results_dir=<local path> --method=<name of the method> --nb_phrases=<number of phrases> --split_size=<split size of text> --max_length=<max length of keyphrases>``

options:
--file: Name of the transcript file from which to extract keywords. Default:'meeting_enhanced.txt'
--data_dir: Path to the folder where to find the file. Default:'./transcripts'
--results_dir: Path to the folder where to save the results to. Default:'./results_kw_extractions'
--method: The method to use for keyword extraction ('rake', 'embedrank' or 'sifrank'). Default:'rake'
--nb_phrases: Number of phrases to detect. Default:'10'
--split_size: Number of sentences in each split (-1 == no split). Default:'10'
--max_length: Max number of words in the keyphrases in output (only for the'rake' method). Default:'3'