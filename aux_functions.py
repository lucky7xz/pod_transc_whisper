import glob
import os
import random
import json
import librosa

def check_folder_content_and_format(folder_name):
    '''
    check for folder file content and format
    if folder contains only wav files, return "wav", len(wav_list)
    if folder contains only mp3 files, return "mp3", len(mp3_list)

    if folder contains files of different formats, return False
    Also return False if folder is empty
    '''

    file_list = glob.glob(folder_name+"/*")
    mp3_list = glob.glob(folder_name+"/*.mp3")
    wav_list = glob.glob(folder_name+"/*.wav")


    if len(file_list) == 0:
        print("\n No files in folder")
        return False

    # there should be either only mp3 with no further files OR
    # only wav files with no further files

    if set(wav_list) == set(file_list):
            
            print("\n Folder contains only wav files. Moving on...")
            return "wav", len(wav_list)
    elif set(mp3_list) == set(file_list):

        print("\n Folder contains only mp3 files. Moving on...")
        return "mp3", len(mp3_list)

    else:
        print("\n Folder contains files of different formats. Please check")
        return False
    

def check_SR_and_duration(folder_name):
    '''
    check sample rate and aprox duration of files in folder
    
    '''

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
        print("\n Not all files have the same sample rate")
        print("This might not be a problem, but it is worth checking")

        sr_ret = "variable"
    else:
        print("\n All files have the same sample rate")
        sr_ret = str(sr_checker)

    avg_duration = round((sum(duration_of_test_picks)/len(duration_of_test_picks)) / 60, 2) 

    return sr_ret, avg_duration


def init_folder_log(folder_name,ep_count,aprox_duration_min, SR):
    
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

    with open("transcription_log.json", "r") as f:
        log = json.load(f)

    log[folder_name] = {"files":{},
                        "aprox_folder_duration_min":aprox_duration_min,
                        "format":format,
                        "sample_rate":SR,
                        "ep_count":ep_count,

                        # Default values when init
                        # split_done might be used later in conjunction witl nemo drill

                        "transc_done":False,
                        "split_done":"Whispered"}

    with open("transcription_log.json", "w") as f:
        json.dump(log, f, indent=4, sort_keys=True)



def update_folder_log_transc_done(folder_name,transc_done=True):


    with open("transcription_log.json", "r") as f:
        log = json.load(f)

    log[folder_name]["transc_done"] = transc_done
    log[folder_name]["trans_time_sec"] = round(sum([key["transc_time"] for key in log[folder_name]["files"].keys()]),2)


    with open("transcription_log.json", "w") as f:
        json.dump(log, f, indent=4, sort_keys=True)



def init_log_file(folder_name, file_name,model_type):

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

    log[folder_name]["files"][file_name] = {"transc_time":"",
                                            "transc_done":False,
                                            "split_done":"Whispered",
                                            "transc_type":model_type,
                                            "title": ""}


    with open("transcription_log.json", "w") as f:
        json.dump(log, f, indent=4, sort_keys=True)

  

def update_file_log(folder_name, file_name, transc_time):

    with open("transcription_log.json", "r") as f:
        log = json.load(f)

    log[folder_name]["files"][file_name]["transc_time"] = transc_time
    log[folder_name]["files"][file_name]["transc_done"] = True

    with open("transcription_log.json", "w") as f:
        json.dump(log, f, indent=4, sort_keys=True)