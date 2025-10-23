
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
from tkinter import simpledialog

"""Welcome message for the users"""
root = tk.Tk()
root.withdraw()  # Hide the main window

tk.messagebox.showinfo(
    "Welcome!",
    "This script will clean your .Pitch files by removing low-confidence pitch candidates.\n\n"
    "You need to select: \n"
    "1. The folder containing your .Pitch files.\n"
    "2. Selection threshold: The confidence level below which pitch candidates will not be selected (i.e., not become pink in Praat).\n"
    "3. Visibility threshold: The confidence levels below which pitch candidates will not be shown at all in Praat.\n\n"
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

""""Selection threshold: Ask the user for the confidence threshold below which pitch candidates will not be selected"""
# Open a dialog box that allows the user to select the pitch selection threshold
# We want a button dialog with options from 1 to 10
confidence_threshold = tk.simpledialog.askinteger(
    "Select pitch selection threshold",
    "Enter the confidence threshold (2-10) below which pitch candidates will not be SELECTED:",
    minvalue=2,
    maxvalue=10
)

if confidence_threshold is None:  # If the user cancels the dialog
    print("No confidence threshold selected. Exiting.")
    exit()

""""Visibility threshold: Ask the user for the confidence threshold below which pitch candidates will not be shown at all"""
# Open a dialog box that allows the user to select the visibility threshold
# We want a button dialog with options from 1 to 10
visibility_threshold = tk.simpledialog.askinteger(
    "Select pitch visibility threshold",
    "Enter the confidence threshold (2-10) below which pitch candidates will not be SHOWN:",
    minvalue=2,
    maxvalue=10
)

if visibility_threshold is None:  # If the user cancels the dialog
    print("No visibility threshold selected. Exiting.")
    exit()

# Convert the thresholds to values that match the strength values in the .Pitch files
confidence_threshold_value = (confidence_threshold - 0.5) / 10.0  # e.g., 8 becomes 0.75
visibility_threshold_value = (visibility_threshold - 0.5) / 10.0  # e.g., 6 becomes 0.55

"""List the files in the folder""" 

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

# For each .Pitch file in the list of pitch files
for i in range(len(pitch_files)):

    # Open the .Pitch file and read its content
    with open(pitch_files[i], encoding="utf-8") as pitchfile:
        read_pitchfile = pitchfile.read()

    # Loop through the lines of read_pitchfile
    lines = read_pitchfile.splitlines()

    # If a line begins with strength, we check whether the strength value is below 0.75
    # If it is, we want to set strength to 0, as well as the corresponding frequency (on the line above)
    for index, line in enumerate(lines):
        if line.startswith('                strength'):
            strength_value = float(line.split()[2]) # The third element is the strength value
            strength_index = index  # Always set strength_index here
            
            if strength_value < confidence_threshold_value:
                
                # Check whether this line is the first candidate (i.e., the pink one in Praat)
                if lines[strength_index-3].startswith('        candidates []:'):

                    # If it is the selected one, we need to update the nCandidates line (1 lines above the candidates [] line)
                    nCandidates_index = strength_index - 4
                    nCandidates_value = int(lines[nCandidates_index].split()[2])  # The third element is the nCandidates value
                    nCandidates_value += 1  # Increase by 1
                    lines[nCandidates_index] = f'        nCandidates = {nCandidates_value} '

                    # If it is the selected one, we need to add a dummy candidate above it
                    lines.insert(strength_index-2, '            candidates [0]:')
                    lines.insert(strength_index-1, '                frequency = 0')
                    lines.insert(strength_index,   '                strength = 0')

            # Next, for candidates below the visibility threshold, set frequency and strength to 0
            if strength_value < visibility_threshold_value:
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