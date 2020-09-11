from google.cloud import speech_v1p1beta1
import io
import json


def sample_long_running_recognize(filename, data_dir="./data", transcript_dir="./transcripts", confidences_dir="./confidences",
    enable_speaker_diarization=True, nb_speakers=1, model=None, enable_word_confidence=True, use_enhanced=False):
    """Reads an audio file and save its transcript as well as the corresponding confidences
    
    Parameters
    ----------
    filename : str
        Name of the file from which the text is loaded.
    data_dir : str
        Path of the folder where to find the file 'filename'.
    transcript_dir : str
        Path to the folder where to save the transcript.
    confidences_dir : str
        Path to the folder where to save confidences results..
    enable_speaker_diarization : bool
        Whether to enable speaker diarization or not.
    nb_speakers : int
        Required size of each part of the text (in number of sentences). (if -1 =>  no split)
    model : str
        The model to use for the transcription. ('none' =>  standard model)
    enable_word_confidence : bool
        Whether to enable word confidence or not.
    use_enhanced : bool
        Whether to use an enhanced model (extra cost) or not.

    """
    client = speech_v1p1beta1.SpeechClient()

    # configurations
    language_code = "en-US"
    config = {
        "enable_speaker_diarization": enable_speaker_diarization,
        "diarization_speaker_count": nb_speakers,
        "language_code": language_code,
        "enable_word_confidence": enable_word_confidence,
        "enable_automatic_punctuation":True,
        "use_enhanced": use_enhanced
    }
    if (model is not None) and (model != "none") :
        config["model"] = model
    
    local_file_path = data_folder_path + "/" + filename
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
 
    # transcript
    print(u"Transcript: {}".format(response.results[0].alternatives[0].transcript))
    
    # diarization
    confidences = {}
    diarized_transcript = ""
    previous_speaker = -1
    current_speaker = -1
    results_list = [response.results[-1]]

    for result in results_list:
    	alternative = result.alternatives[0]
    	for word in alternative.words:
    		current_speaker = word.speaker_tag
    		if (current_speaker != previous_speaker):
    			previous_speaker = current_speaker
    			diarized_transcript += "\n[" + str(previous_speaker) + "]\n"
    		diarized_transcript += word.word + " "
    		if enable_word_confidence:
    			confidences[word.word] = word.confidence

    # report transcript in new file
    transcript_path = transcript_dir + "/transcript_" + filename.split(".")[0] + ".txt"
    with open(transcript_path, 'w') as transcript_file:
        transcript_file.write(diarized_transcript)

    # report confidences
    if enable_word_confidence:
        confidences_path = confidences_dir + "/confidences_" + filename.split(".")[0] + ".txt"
        with open(confidences_path, 'w') as confidence_file:
            json.dump(confidences, confidence_file)






