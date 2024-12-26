import random
import pkg_resources
from IPython.display import Audio, display  # Ensure display is imported
from playsound import playsound

def play_finish_sound_notebook():
    """
    Plays a random finish sound from the package's resources using browser-based audio in Colab.
    """
    # List all files in the 'sounds' directory
    sound_files = pkg_resources.resource_listdir("finish_sound", "sounds")
    
    # Filter out only .mp3 files
    mp3_files = [file for file in sound_files if file.endswith(".mp3")]
    
    # Select a random file from the list
    random_sound = random.choice(mp3_files)
    
    # Get the full path to the randomly selected sound file
    sound_file = pkg_resources.resource_filename(
        "finish_sound", f"sounds/{random_sound}"
    )
    
    # Use IPython display to play the sound in the notebook
    display(Audio(sound_file))


def play_finish_sound():
    """
    Plays a random finish sound from the package's resources.
    """
    # List all files in the 'sounds' directory
    sound_files = pkg_resources.resource_listdir("finish_sound", "sounds")
    
    # Filter out only .mp3 files
    mp3_files = [file for file in sound_files if file.endswith(".mp3")]
    
    # Select a random file from the list
    random_sound = random.choice(mp3_files)
    
    # Get the full path to the randomly selected sound file
    sound_file = pkg_resources.resource_filename(
        "finish_sound", f"sounds/{random_sound}"
    )
    
    # print(f"Code finished. Playing sound: {random_sound}")
    playsound(sound_file)
