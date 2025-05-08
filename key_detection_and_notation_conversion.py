# Library Imports
from chord_extractor.extractors import Chordino
import sys


### Structure Definitions :

def array_add(*args): # Takes arrays of same length as input to be added
    sum_arr = []
    try:
        for arr in args:
            if len(arr) != len(args[0]):
                print("Arrays are not of same length.")
                return
	
        for i in range(0,len(args[0])):
            temp_sum = 0
            for arr in args:
                temp_sum += arr[i]
            sum_arr.append(temp_sum)

        return sum_arr

    except:
        print("Error in args, please check input.")
        return

def cyclic_shift(array, num, left = 0): # shifts the positions of an array cyclicly
    try:
        temp_arr = array.copy() # Creates a shallow copy
        if left == 0:
            for i in range(0,num):
                temp_arr = [temp_arr[-1]] + temp_arr[:-1]
        elif left == 1:
            for i in range(0,num):
                temp_arr =temp_arr[1:] + [temp_arr[0]]
        else:
            print("Error with 'left' value.")
            return
        return temp_arr

    except:
        print("Error in array or num, please check input.")
        return
	    
# Chordino extraction tool
chordino = Chordino(roll_on=1)  

scales = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']



### Chord Extraction :


#song_location = r"C:\Users\srina\Music\morgan powers - Disarray.mp3"
#song_location = r"C:\Users\srina\Music\Viva La Vida or Death And All Of His Friends\07. Viva La Vida.mp3"
#song_location = r"C:\Users\srina\Music\A Rush Of Blood To The Head (2002)\03-coldplay-god_put_a_smile_upon_your_face.mp3"
#song_location = r"C:\Users\srina\Music\Parachutes (2000)\05 Yellow.m4a"
song_location = r"C:\Users\srina\Music\A Rush Of Blood To The Head (2002)\04-coldplay-the_scientist.mp3"
print(song_location)

#new_file_path = chordino.preprocess(r'C:\Users\srina\Music\Parachutes (2000)\05 Yellow.m4a')
#new_file_path = chordino.preprocess(song_location)
chords = chordino.extract(song_location)
'''
try:
    chords = chordino.extract(song_location)
except:
    print("There was an error extracting from this file. Terminating program...")
    new_file_path = chordino.preprocess(song_location)
    chords = chordino.extract(new_file_path)
'''

raw_chord_list = []
raw_times_list = []
for i in range(0,len(chords)):
    #print(i)
    raw_chord_list.append(chords[i].chord)
    raw_times_list.append(float("{:.3f}".format(chords[i].timestamp)))

#print(chord_list,"\n\n",times_list)
song_info = song_location.split("\\")[-1]
#print(song_info)
    
print()

chord_list = []
times_list = []
# refining chord list:
for i in range(0,len(raw_chord_list)):
    ch = raw_chord_list[i]
    if ch == 'N':
        continue
    if 'maj' in ch:
        ch = ch.replace('maj','')
    chord_list.append(ch)
    times_list.append(raw_times_list[i])


### Key Signature estimation :


scales_used = [0,0,0,0,0,0,0,0,0,0,0,0]
for raw_chord in chord_list:

    chord = raw_chord[0]
    if chord == 'N':
        continue
    if len(raw_chord)>1 :
        if raw_chord[1] == '#' or raw_chord[1] == 'b':
            chord += raw_chord[1]
            if raw_chord[1] == 'b':
                transfer = ['Ab','Bb','Db','Eb','Gb'].index(chord)
                chord = ['G#','A#','C#','D#','F#'][transfer]
            if len(raw_chord)>2:
                if raw_chord[2] == 'm':
                    chord +=raw_chord[2]
        elif raw_chord[1] == 'm':
            chord += raw_chord[1]

    #print(raw_chord, chord)
    
    is_minor = int(any(x=="m" for x in chord))
    if 'm' in chord:
        position_difference = scales.index(chord[:-1])
    else:
        position_difference = scales.index(chord)
    sequence = [ [1,1,0,0,0,1,0,1,0,0,0,0] , [0,1,0,1,0,0,0,0,1,0,1,0] ][is_minor]
    scale_array = cyclic_shift(sequence, position_difference)
    scales_used = array_add(scales_used, scale_array)

print(scales_used, max(scales_used), len(chord_list))
key_signature_pos = scales_used.index(max(scales_used))
key_signature = scales[key_signature_pos]
print(f"Key signature : {key_signature} (or {scales[(key_signature_pos-3)%12]}m)")



### Chord Progression notation conversion :

key_scale = scales.copy()
position_difference = scales.index(key_signature)
key_scale = cyclic_shift(key_scale, position_difference, left=1)
#print(key_scale)

progression_list = []
roman_progressions = ['I','bII','II','bIII','III','IV','bV','V','bVI','VI','bVII','VII']
scales_alphabetical = scales.copy()
scales_alphabetical.sort()

for chord in chord_list: # going through each chord one by one

    #print(f"chord {chord} :")
    if len(chord)>1 and chord[1]=='b':
        #print(chord, end = ' | ')
        transfer = ['Ab','Bb','Db','Eb','Gb'].index(chord[:2])
        chord = ['G#','A#','C#','D#','F#'][transfer] + chord[2:]
        #print(chord)

    for note in scales_alphabetical[::-1]: # checking all notes of the scale
        if note in chord: # when note of scale is in the extracted chord
            note_position = key_scale.index(note)
            roman_notation = roman_progressions[note_position]
            if 'm' in chord:
                roman_notation = roman_notation.lower()
            progression_list.append(roman_notation)
            break
            
print(key_scale)
print(roman_progressions)
print(len(chord_list), len(progression_list))
'''
for i in range(0,len(chord_list)):
    print(f"chord {chord_list[i]} is {progression_list[i]}")
    pass

for i in range(0,len(chords)):
    print(f"Chord = {raw_chord_list[i]}, at time {raw_times_list[i]}.")
'''
for i in range(0, len(chord_list)):
    print(f"Chord : {chord_list[i]}, Roman : {progression_list[i]}, Time : {times_list[i]}")
    

print("\nEnd of computation!")
