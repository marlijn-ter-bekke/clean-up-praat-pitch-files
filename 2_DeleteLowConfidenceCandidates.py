
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

"""Set the paths to the .Pitch files"""
### Where is your folder that contains the .Pitch files that need to be cleaned?
pitch_dir = os.path.join('S:\\', 'workspaces', 'cosi-coact', 'working_data', 
                          'coact+', 'corpus_analyses', 'Marlijn', 
                          'prosody', '2_manual_pitch_correction', '3_practice')


"""From here on, you don't need to change anything in the script.""" 

### List the .Pitch files in the folder
pitch_files = sorted(glob.glob(os.path.join(pitch_dir, '*.Pitch'), recursive=False))
# Recursive is false because I only want to look in this folder, not subfolders

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
    
    print(f"Processed file {i+1}/{len(pitch_files)}: {cleaned_pitchfile_path}")

print(f"Saved all cleaned pitch files to {pitch_dir} with _cleaned.Pitch suffix.")