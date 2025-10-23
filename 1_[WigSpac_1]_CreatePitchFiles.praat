# TITLE: 	Creating Pitch files for .wav files

# INPUT: 	given .wav file(s)
# ELABORATION: 	compute pitch track
# OUTPUT: 	save as .Pitch file in the same folder
# NOTES: 	Working on Praat 6.4.43 under Windows Server 2019 Standard
# AUTHOR: 	marlijn.terbekke@donders.ru.nl

# INPUT
form Input parameters
	comment path (with final slash)
	sentence directory \\data\cosi\workspaces\cosi-coact\working_data\coact+\corpus_analyses\Marlijn\prosody\2_manual_pitch_correction\3_practice\
	comment advanced extraction parameters (from MAUSMOOTH)
	integer smooth1 10
	integer smooth2 10
	integer timestep 0
	integer pitchmin 50
	integer pitchmax 450
	integer maxcandidates 15
	real silenceThr 0.03
	real voicingThr 0.45
	real octave 0.01
	real octavejump 0.35
	real voiceunvoiced 0.14 
endform 
Erase all

# OPEN FILES
Create Strings as file list: "pitchlist", directory$+"*.Pitch"
Create Strings as file list: "list", directory$+"*.wav"
Sort
nfile = Get number of strings
for i to nfile
	name$ = Get string: i
	basename$ = name$ - ".wav"
	subject$ = left$ (basename$,3)
	Read from file: directory$+name$

	# CREATE PITCH OBJECTS 

	# COMPUTE PITCH
	To Pitch (ac): timestep, pitchmin, maxcandidates, "no", silenceThr, voicingThr, octave, octavejump, voiceunvoiced, pitchmax

	# DOES .PITCH ALREADY EXIST?
	exists = 0
	selectObject: "Strings pitchlist"
	npitch = Get number of strings
	for k to npitch
		pitchname$ = Get string: k
		pitchbasename$ = pitchname$ - ".Pitch"
		if pitchbasename$ = basename$
			exists = 1
		endif
	endfor

	# IF NOT, CREATE UT
	if exists = 0
		selectObject: "Pitch "+basename$
		Copy: basename$
		Save as text file: directory$+basename$+".Pitch"
	endif

# CLOSE AND CLEAN
	select all
	minusObject: "Strings list"
	minusObject: "Strings pitchlist"
	Remove
	selectObject: "Strings list"
endfor
plusObject: "Strings pitchlist"
Remove
