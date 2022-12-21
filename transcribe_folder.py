import glob
import os
import json
import time

from aux_functions import init_file_in_log, update_file_in_log
from aux_functions import init_model

def transcribe_folder(folder_name, model_type):

    model, model_type = init_model(model_type)

    #read log
    with open("transcription_log.json", "r") as f:
        log = json.load(f)

    format = log[folder_name]["format"]

    # We know folder_name is in file log and transcription of the overall folder is NOT done
    # Check which files (if any) are already done and create iteration list
    #-----------------------------------------------------------------------
    
    #check if log[folder_name]["files"] is empty, if so, init all files
    # Also create folder for transcriptions

    if not log[folder_name]["files"]:

        # glob all files in folder
        audio_files = glob.glob(f'{folder_name}/*')

        #init all audio files in log

        for audio_file in audio_files:
            file_name = os.path.basename(audio_file)

            init_file_in_log(folder_name, file_name, model_type)
        
        iteration_path_list = audio_files
    
        destination_folder = folder_name+"_text"
        os.makedirs(destination_folder)
    
    # if log[folder_name]["files"] is not empty, check which files are done and create iteration list
    else:
        iteration_path_list = []

        for file_name in log[folder_name]["files"].keys():
            if log[folder_name]["files"][file_name]["transc_done"] == False:
                
                # use join path to use on any os
                iteration_path_list.append(os.path.join(folder_name, file_name))

    #-----------------------------------------------------------------------
    
    iteration_list_length = len(iteration_path_list)
    count = 1

    for file_path in iteration_path_list:
        
        # Start timer
        start_time = time.time()

        print(f"\nTranscribing {file_path}...")

        file_name = os.path.basename(file_path)
        destination_folder = folder_name + "_text"
        ext = "." + format

        result = model.transcribe(file_path)
        result_text = result["text"]
        
        #save transcription to file

        transc_path = os.path.join(destination_folder, file_name).replace(ext, '.txt')

        transc_time = time.time() - start_time
        print(f"Transcription of {file_path} done in {transc_time} seconds.")

        with open(transc_path, 'w') as f:
            f.write(result_text)
        print(f"Transcription saved to {transc_path}.")
        
        #update log
        update_file_in_log(folder_name, file_name, transc_time)
      
        
        print(f"Transcription log updated for {file_path}. Progress : {count} / {iteration_list_length}\n")
        count += 1