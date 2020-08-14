from google.cloud import speech_v1p1beta1
import io

import pdb


def sample_long_running_recognize(filename="two_seconds_recording.wav",
    data_folder_path="./data", transcript_folder_path="./transcripts",
    enable_speaker_diarization=True, diarization_speaker_count=3,
    model=None):
    """This function reads a file in the 'data' folder and writes the corresponding transcript in the 'transcripts' folder."""
    
    client = speech_v1p1beta1.SpeechClient()

    # configurations
    language_code = "en-US"
    config = {
        "enable_speaker_diarization": enable_speaker_diarization,
        "diarization_speaker_count": diarization_speaker_count,
        "language_code": language_code
    }
    if model is not None:
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
    result = response.results[1]
    alternative = result.alternatives[0]
    diarized_transcript = ""
    previous_speaker = -1
    current_speaker = -1
    for word in alternative.words:
        current_speaker = word.speaker_tag
        if (current_speaker != previous_speaker):
            previous_speaker = current_speaker
            diarized_transcript += "\n[" + str(previous_speaker) + "]\n"
        diarized_transcript += word.word + " "

    transcript_name = transcript_folder_path + "/transcript_" + filename.split(".")[0] + ".txt"
    with open(transcript_name, 'w') as transcript_file:
        transcript_file.write(diarized_transcript)







