
"""
    Goal of script: 
        - Load in .Pitch files with Praat-generated pitch tracks
        - Remove low confidence pitch candidates automatically (strength below 0.75)
        - Save as _cleaned.Pitch files
    These cleaned files can then be used for manual pitch correction in Praat.
    
    Author: Marlijn ter Bekke
    Creation date: September 2025
    Last updated: October 2025
"""

"""Load packages we need for the script"""
### Load packages
import os
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

"""Welcome message for the users"""
root = tk.Tk()
root.withdraw()  # Hide the main window

tk.messagebox.showinfo(
    "Welcome!",
    "This script will clean your .Pitch files by removing low-confidence pitch candidates (confidence < 8).\n\n"
    "You first need to select the folder containing your .Pitch files.\n"
    "The script will then process the .Pitch files in this folder and save cleaned versions with '_cleaned.Pitch' suffix.\n\n"
    "If there are already files ending with '_cleaned.Pitch' in the folder, these will be overwritten.\n\n"
    "Click OK to continue."
)

"""Set the paths to the .Pitch files"""
### Where is your folder that contains the .Pitch files that need to be cleaned?

# Open a dialog box for the user to select the folder
pitch_dir = filedialog.askdirectory(title="Select the folder containing .Pitch files")
if not pitch_dir:  # If the user cancels the dialog
    print("No folder selected. Exiting.")
    exit()

"""From here on, you don't need to change anything in the script.""" 

### List the .Pitch files in the folder
pitch_files = sorted(glob.glob(os.path.join(pitch_dir, '*.Pitch'), recursive=False))
# Recursive is false because I only want to look in this folder, not subfolders

if not pitch_files:
    print("No .Pitch files found in the selected folder. Exiting.")
    exit()

# Exclude files ending with '_cleaned.Pitch', we don't want to process those again
pitch_files = [f for f in pitch_files if not f.endswith('_cleaned.Pitch')]

""" Create a progress window """ 
progress_window = tk.Toplevel(root)
progress_window.title("Processing Files")
progress_label = tk.Label(progress_window, text="Starting...", padx=20, pady=10)
progress_label.pack()

"""Open each .Pitch file and delete low confidence pitch candidates (strength below 0.75)"""
# We choose strength (confidence) 0.75 as the threshold, because 0.75 will be rounded up to 0.8 and displayed as a confidence value of 8 in Praat

# For each .Pitch file in the list of pitch files
for i in range(len(pitch_files)):

    # Open the .Pitch file and read its content
    with open(pitch_files[i], encoding="utf-8") as pitchfile:
        read_pitchfile = pitchfile.read()

    # We can check that the original file has been automatically closed
    pitchfile.closed

    # Loop through the lines of read_pitchfile
    lines = read_pitchfile.splitlines()

    # If a line begins with strength, we check whether the strength value is below 0.75
    # If it is, we want to set strength to 0, as well as the corresponding frequency (on the line above)
    for line in lines:
        if line.startswith('                strength'):
            strength_value = float(line.split()[2]) # The third element is the strength value
            if strength_value < 0.75:
                # Get the index of this line (strength line)
                strength_index = lines.index(line) 
                # Set this line to strength 0
                lines[strength_index] = '                strength = 0 '    
                # Get the index of the previous line (frequency line)
                frequency_index = strength_index - 1   
                # Set this line to frequency 0 
                lines[frequency_index] = '                frequency = 0 '  

    # Save the cleaned .Pitch file as a new file with _cleaned.Pitch suffix
    cleaned_pitchfile_path = pitch_files[i].replace('.Pitch', '_cleaned.Pitch')
    with open(cleaned_pitchfile_path, 'w', encoding="utf-8") as cleaned_pitchfile:
        for line in lines:
            cleaned_pitchfile.write(line + '\n')
    
    # Update progress label
    progress_label.config(text=f"Processing file {i+1}/{len(pitch_files)}: {os.path.basename(pitch_files[i])}")
    progress_window.update()  # Force the window to update

# Close the progress window
progress_window.destroy()

# Show completion message
messagebox.showinfo(
    "Done!",
    f"All files have been processed and saved with '_cleaned.Pitch' suffix in:\n{pitch_dir}\n\n"
    "You can now use the cleaned files in Praat."
)