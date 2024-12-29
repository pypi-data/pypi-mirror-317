import os
import time
import subprocess
import sys
import importlib.resources
from pathlib import Path
from plyer import notification
from playsound import playsound

# def get_sound_file(file_name):
#     return importlib.resources.files('src.sound_effects') / file_name

def print_elapsed_time(elapsed_time):
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Command completed successfully.")
    print(f"Execution Time: ")
    if hours>0 :
        print(f"{int(hours):02} hours")
    if minutes>0 :
        print(f"{int(minutes):02} minutes")
    if seconds>0 :
        print(f"{seconds:.2f} seconds")

def run_command_with_notification():
    if len(sys.argv) < 2:
        print("Usage: notify <command> [args...]")
        sys.exit(1)

    # The command to run
    command = sys.argv[1:]
    success_tone = str(importlib.resources.files('src').joinpath("sound_effects", "success.wav"));
    error_tone = str(importlib.resources.files('src').joinpath("sound_effects", "error.wav"));

    try:
        start_time = time.time()
        process = subprocess.run(command, check=True, shell=True)   # Run the terminal command
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_elapsed_time(elapsed_time)
        notification.notify(
            title="Command executed successfully",
            message=f"{' '.join(command)} done!",
            app_name="ti-ding notifier",
            timeout=5
        )
        # Play the notification sound
        playsound(success_tone)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}.")
        playsound(error_tone)  
    except Exception as e:
        print(f"An error occurred: {e}")
        playsound(error_tone)  

