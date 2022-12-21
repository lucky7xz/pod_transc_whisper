import glob
import os
import random
import json
import librosa
import whisper

def check_folder_content_and_format(folder_name):
    '''
    check for folder file content and format
    if folder contains only wav files, return "wav", len(wav_list)
    if folder contains only mp3 files, return "mp3", len(mp3_list)

    if folder contains files of different formats, return False
    Also return False if folder is empty
    '''

    print(f"\n Checking folder {folder_name} for content and format...")

    file_list = glob.glob(folder_name+"/*")
    mp3_list = glob.glob(folder_name+"/*.mp3")
    wav_list = glob.glob(folder_name+"/*.wav")


    if len(file_list) == 0:
        print("\n No files in folder. Please check and try again")
        return False, -1

    # there should be either only mp3 with no further files OR
    # only wav files with no further files

    if set(wav_list) == set(file_list):
            
            print("--- Folder contains only wav files. Moving on...")
            return "wav", len(wav_list)
    elif set(mp3_list) == set(file_list):

        print("---Folder contains only mp3 files. Moving on...")
        return "mp3", len(mp3_list)

    else:
        print("---Folder contains files of different formats. Please check and try again")
        return False, -1
    

def check_SR_and_duration(folder_name):
    '''
    check sample rate and aprox duration of files in folder
    
    '''

    print(f"\n Checking sample rate and aprox avg duration of files in folder {folder_name}...")
    file_list = glob.glob(folder_name+"/*")

    test_picks = [random.choice(file_list), # pick 7 random files
                  random.choice(file_list),
                  random.choice(file_list),
                  random.choice(file_list),
                  random.choice(file_list),
                  random.choice(file_list),
                  random.choice(file_list)]

    sr_of_test_picks = [librosa.get_samplerate(test_pick) for test_pick in test_picks]
    duration_of_test_picks = [librosa.get_duration(filename=test_pick) for test_pick in test_picks]


     
    sr_checker = sr_of_test_picks[0]
    if not all(sr_checker == sr for sr in sr_of_test_picks):
        print("--- Not all files have the same sample rate")
        print("This might not be a problem, but it is worth checking")

        sr_ret = -1
    else:
        print("--- All files have the same sample rate")
        sr_ret = sr_checker

    aprox_avg_ep_duration_min = round((sum(duration_of_test_picks)/len(duration_of_test_picks)) / 60, 2) 

    return sr_ret, aprox_avg_ep_duration_min


def init_folder_log(folder_name):
    
    '''
    init a folder log entry with the following:
    
    folder_name
    files: {}
    aprox_folder_duration_min
    format
    sample_rate
    ep_count
    transc_done: False
    split_done: False
    
    '''

    format, ep_count = check_folder_content_and_format(folder_name)

    if format != False:
            
        SR, aprox_avg_ep_duration_min = check_SR_and_duration(folder_name)
    

        with open("transcription_log.json", "r") as f:
            log = json.load(f)

        log[folder_name] = {"files":{},
                            "aprox_avg_ep_duration_min":aprox_avg_ep_duration_min,
                            "format":format,
                            "sample_rate":SR,
                            "ep_count":ep_count,

                            # Default values when init
                            # split_done might be used later in conjunction witl nemo drill

                            "transc_done":False,
                            "split_done":"Whispered"}

        with open("transcription_log.json", "w") as f:
            json.dump(log, f, indent=4, sort_keys=True)

    else:
        #Raise errror to terminate program
        raise ValueError(f"Folder {folder_name} not init in log file because of content format error.")
        


def update_folder_log(folder_name):


    with open("transcription_log.json", "r") as f:
        log = json.load(f)

    log[folder_name]["transc_done"] = True
    log[folder_name]["trans_time_sec"] = round(sum([key["transc_time_sec"] for key in log[folder_name]["files"].keys()]),2) #***


    with open("transcription_log.json", "w") as f:
        json.dump(log, f, indent=4, sort_keys=True)



def init_file_in_log(folder_name, file_name):

    '''
    Init a file log entry with the following:
    
    title: ""
    transc_type: model_type
    transc_time: ""
    transc_done: False
    split_done: Whispered
    
    '''
    with open("transcription_log.json", "r") as f:
        log = json.load(f)

    log[folder_name]["files"][file_name] = {"transc_time_sec":-1,
                                            "transc_done":False,
                                            "split_done":"Whispered",
                                            "transc_type":"",
                                            "title": ""}


    with open("transcription_log.json", "w") as f:
        json.dump(log, f, indent=4, sort_keys=True)

  

def update_file_in_log(folder_name, file_name, transc_time, model_type):

    with open("transcription_log.json", "r") as f:
        log = json.load(f)

    log[folder_name]["files"][file_name]["transc_time_sec"] = transc_time
    log[folder_name]["files"][file_name]["transc_done"] = True
    log[folder_name]["files"][file_name]["transc_type"] = model_type

    with open("transcription_log.json", "w") as f:
        json.dump(log, f, indent=4, sort_keys=True)


# Run MODEL def with specific config ?

def init_model(model_type):


    if model_type == "tiny":
        model = whisper.load_model("tiny")

    elif model_type == "base":
        model = model = whisper.load_model("base")

    elif model_type == "medium":
        model = model = whisper.load_model("medium")
    
    else:
        raise ValueError("model_type must be 'tiny' or 'base' or medium")

    return model, model_type


def check_log_and_podcast_folder_file():

# ----- Check if podcast_folders.txt exists, if it does, read the file -----

    if os.path.exists('podcast_folders.txt'):

        with open('podcast_folders.txt', 'r') as f:
            folder_names = f.read().splitlines()

        folder_names = [folder_name.strip() for folder_name in folder_names]
        folder_names = [folder_name for folder_name in folder_names if folder_name != ""]
        folder_names = [folder_name for folder_name in folder_names if folder_name[0] != "#"]
        

    else:
        raise ValueError("podcast_folders.txt does not exist. Please and try again.")


    # ---- Check if log file exists, if it does, read the log file ----
    if os.path.exists('transcription_log.json'):
        with open('transcription_log.json', 'r') as f:
            log = json.load(f)
    else:

    #otherwise create init log file
        data = {}

        with open('transcription_log.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        
        with open('transcription_log.json', 'r') as f:
            log = json.load(f)


    return folder_names, log
#------------------------------------------------------------