from google.cloud import speech_v1p1beta1
import io
import json


def sample_long_running_recognize(filename,
    data_folder_path="./data", transcript_folder_path="./transcripts",
    confidences_folder_path = "./confidences",
    enable_speaker_diarization=True, diarization_speaker_count=1,
    model=None, enable_word_confidence=True, use_enhanced=False):
    """This function reads an audio file and reports its transcript and the corresponding confidences"""
    
    client = speech_v1p1beta1.SpeechClient()

    # configurations
    language_code = "en-US"
    config = {
        "enable_speaker_diarization": enable_speaker_diarization,
        "diarization_speaker_count": diarization_speaker_count,
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
    transcript_path = transcript_folder_path + "/transcript_" + filename.split(".")[0] + ".txt"
    with open(transcript_path, 'w') as transcript_file:
        transcript_file.write(diarized_transcript)

    # report confidences
    if enable_word_confidence:
        confidences_path = confidences_folder_path + "/confidences_" + filename.split(".")[0] + ".txt"
        with open(confidences_path, 'w') as confidence_file:
            json.dump(confidences, confidence_file)






