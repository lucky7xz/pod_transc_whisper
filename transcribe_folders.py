import glob
import os
import json
import time
import librosa

import whisper


# Read the text file with the podcast folder names
with open('podcast_folders.txt', 'r') as f:
    folder_names = f.read().splitlines()


# check if log file exists
# If it does, read the log file
if os.path.exists('log.txt'):
    with open('log.txt', 'r') as f:
        progress = json.load(f)
else:
   
   #otherwise create a new log file

   with open('log.txt', 'w') as f:
        json.dump("{}", f, indent=4)
    






# Create a dictionary to track the progress


# Iterate through the folders
for folder_name in folder_names:
    # Create a folder for the transcriptions
    transcription_folder = f'{folder}_text'
    os.makedirs(transcription_folder, exist_ok=True)

    # Find all audio files in the folder
    audio_files = glob.glob(f'{folder}/*')

    # Iterate through the audio files
    for audio_file in audio_files:
        # Run the audio file through whisper transcribe
        transcription = whisper_transcribe(audio_file)

        # Save the transcription to a text file with the same name as the audio file
        transcription_file = os.path.join(transcription_folder, os.path.basename(audio_file)).replace('.mp3', '.txt')
        with open(transcription_file, 'w') as f:
            f.write(transcription)



    
    #--------  update log for podcast folder
    with open("transcription_log.json", "r") as f:
            log = json.load(f)

    log[folder_name]["transc_done"] = True
    log[folder_name]["ep_count"] = len(log[folder_name]["files"].keys())
    log[folder_name]["tramsc_type"] = select_model
            
    with open("transcription_log.json", "w") as f:
            json.dump(log, f, indent=4, sort_keys=True)
    #--------------------

    print("Folder", folder_name, "transcribed. Progress:", fcount, "/", length)
   

