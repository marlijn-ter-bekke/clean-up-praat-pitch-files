# TITLE: 		MAUSMOOTH (Manual and AUtomatic SMOOTHing of f0 tracks)

# INPUT: 		.wav files and corresponding _cleaned.Pitch files
# OUTPUT: 		Manual correction as .Pitch file and smoothed contour as .smooth file
# NOTES: 		If there is no manual correction (*_manual.Pitch file) available,
#				the script asks user to create a new one (pausing the script for each file)
# 				Working on Praat 6.4.43 under Microsoft Windows Server 2019 Standard
# AUTHOR: 		fcangemi@uni-koeln.de
# ADJUSTED BY: 	Marlijn ter Bekke, marlijnterbekke.nl 
# LAST UPDATE: 	2025-OCT-16

# INPUT
form Input parameters
	
	comment path (with final slash)
	sentence directory \\data\cosi\workspaces\cosi-coact\working_data\coact+\corpus_analyses\Marlijn\prosody\3_wigspac\5_test_01A_task2\
	comment advanced extraction parameters
	integer smooth1 10
	integer smooth2 10

endform 

Erase all

# OPEN FILES
writeInfoLine: "Running script in directory: ", directory$
Create Strings as file list: "pitchlist", directory$+"*_cleaned.Pitch"
Create Strings as file list: "list", directory$+"*.wav"
Sort
nfile = Get number of strings

for i to nfile

	name$ = Get string: i
	basename$ = name$ - ".wav"
	
# MANUAL CORRECTION AND SMOOTHING
	# does a _manual.Pitch file already exist?
	
	# set variable exists to 0 as initial value
	exists = 0 
	
	# create the name of the manual pitch file
	manualname$ = basename$+"_manual.Pitch"

	# create strings list of manual pitch files in the directory
	Create Strings as file list: "manualpitchlist", directory$+"*_manual.Pitch"
	selectObject: "Strings manualpitchlist"
	npitch = Get number of strings
	
	# for each name in the manualpitchlist, check if it matches the current manualname$
	for k to npitch
		
		existingmanualpitchname$ = Get string: k
		
		if existingmanualpitchname$ == manualname$
		
			exists = 1
		
		endif
	
	endfor

	# if a _manual file already exists, skip to the next file
	if exists == 1

		appendInfoLine ("Skipping file: ", basename$)
		
	endif

	# if it doesn't exist, then create it
	if exists == 0

		# open .wav file
		Read from file: directory$+name$
		View & Edit
		
		# open _cleaned.Pitch file
		Read from file: directory$+basename$+"_cleaned.Pitch"
		selectObject: "Pitch "+basename$+"_cleaned"
		Copy: basename$
	
		# A. MANUAL CORRECTION
		View & Edit
		pause Confirm
	
		# save the manual correction
		Rename: "manual"
		Save as text file: directory$+basename$+"_manual.Pitch"

		# B. SMOOTHING
		Smooth: smooth1
		Rename: "smooth"
		Interpolate
		Smooth: smooth2
		Rename: "smooth"
		Save as text file: directory$+basename$+".smooth"

	endif
	
# close loops and clean
	select all
	minusObject: "Strings list"
	minusObject: "Strings pitchlist"
	minusObject: "Strings manualpitchlist"
	
	# If after this selection and deselection there are still objects selected, then remove them
	if numberOfSelected() > 0
		Remove
	endif

	selectObject: "Strings list"

	appendInfoLine: "Finished processing file ", i, " out of ", nfile, "."

endfor

appendInfoLine: "Script finished, processed ", (i-1), " files."

# at the end of the loop, also clean the String lists
plusObject: "Strings pitchlist"
plusObject: "Strings manualpitchlist"
plusObject: "Strings list"
Remove