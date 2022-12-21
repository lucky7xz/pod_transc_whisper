

from aux_functions import check_log_and_podcast_folder_file
from aux_functions import init_folder_log, update_folder_log

from transcribe_folder import transcribe_folder
import time

# aprox_avg_ep_duration !!
# transc type update when winished, not init!!

# ---- Select the model to use !!! ---

model_type = "tiny" # "tiny", "base" or "medium"

# Check if log file exists and if podcast folder file exists, load them
folder_names, log = check_log_and_podcast_folder_file()

#-------------------------------------

#check if log is empty
if not log:

    # if so, init folder entry in log for each folder
    for folder_name in folder_names:

         
        init_folder_log(folder_name) # use use check functions for format, if not correct, raise error
        print(f"Folder {folder_name} init in log file.")


    # set the iteration variable
    iteration_list = folder_names


# if log is not empty, check which folders are done and create iteration list
else:

    

    # but first update the log with the new folders
    for folder_name in folder_names:
        
        if folder_name not in log.keys():
            init_folder_log(folder_name)
            print(f" --------- Folder {folder_name} init in log file.[+] --------- ")

    
    iteration_list = []

    for folder_name in folder_names:
        if log[folder_name]["transc_done"] == False:
            iteration_list.append(folder_name)


# iterate over folders in iteration list and start transcription

count = 1
for folder_name in iteration_list:

    #start timer
    start_time = time.time()

    transcribe_folder(folder_name, model_type)

    #update log
    update_folder_log(folder_name)
    print(f"Folder {folder_name} updated in log file. Progress : {count} / {len(iteration_list)}")

    # print time
    print(f"Transcription of folder {folder_name} done in {time.time() - start_time} seconds.")
    print("Note that some files may have been skipped if they were already transcribed. Check the log file for more info.\n")