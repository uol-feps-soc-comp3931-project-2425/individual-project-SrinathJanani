# Library Imports
#from chord_extractor.extractors import Chordino
import sys


### Structured Definitions

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

scales = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
#scales_minor = [key+'m' for key in scales_major]
roman_progressions = ['I','bII','II','bIII','III','IV','bV','V','bVI','VI','bVII','VII']
minor_scale = ['I','#I','II','III','#III','IV','#IV','V','VI','#VI','VII','#VII']
major_scale = ['I','#I','II','#II','III','IV','#IV','V','#V','VI','#VI','VII']


def CleanChord(chord, full_clean = 0):

    # Basic validity checking:
    if chord[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'N']:
        print("Error in cleaning: Invalid chord notation detected.")

    # Cleaning complexity from chord names
    if 'maj' in chord:
        chord = chord.replace('maj','')
    if 'sus' in chord:
        chord = chord.replace('sus','')

    # Just representing note and major/minor
    if full_clean == 1:
        
        clean_chord = chord[0]
        if len(chord)>1 :
            
            if chord[1] == '#' or chord[1] == 'b':
                clean_chord += chord[1]
                if chord[1] == 'b':
                    # Transferring to a common notation of using # replacing b
                    transfer = ['Ab','Bb','Db','Eb','Gb'].index(clean_chord)
                    clean_chord = ['G#','A#','C#','D#','F#'][transfer]
                if len(chord)>2:
                    if chord[2] == 'm':
                        clean_chord += chord[2]
                        
            elif chord[1] == 'm':
                clean_chord += chord[1]

        return clean_chord
    return chord


def GetScale(key):

    key_scale = scales
    if 'm' in key:
        key = key[:-1]

    position_difference = key_scale.index(key)
    key_scale = cyclic_shift(key_scale, position_difference, left = 1)

    return key_scale

def ConvertToRoman(chords_arr, key):

    chosen_roman = major_scale
    if 'm' in key:
        key = key[:-1]
        chosen_roman = minor_scale
    key_scale = GetScale(key)

    edited_arr = []

    for chord in chords_arr:

        try:
            is_minor = 0
            if 'm' in chord:
                is_minor = 1
                chord = chord[:-1]

            if len(chord)>1 and chord[1]=='b':
                transfer = ['Ab','Bb','Db','Eb','Gb'].index(chord[:2])
                chord = ['G#','A#','C#','D#','F#'][transfer] + chord[2:]
                
            note_position = key_scale.index(chord)
            roman_notation = chosen_roman[note_position]#roman_progressions[note_position] # use chosen_roman instead
            if is_minor == 1:
                roman_notation = roman_notation.lower()
            edited_arr.append(roman_notation)

        except:
            print("Error in ConvertToRoman: Chord not found in possible chords array.")
            
    return edited_arr


# Array to enumerate chords, based on frequency of appearance in music

EnumerateChords = [ 
    'I','IV','V','vi','ii','iii','II','vii',
    'i','VI','VII','III','iv','v','bVII','bVI',
    'bIII','bII','bvii','bV','bv','biii','bvi','bii'
    ] # first row = major scale chords, second row = minor scale chords, third row = out-of-scale chords
