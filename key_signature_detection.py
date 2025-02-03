# Library Imports
from chord_extractor.extractors import Chordino


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



# Extracting from location
#song_location = r"C:\Users\srina\Music\morgan powers - Disarray.mp3"
#song_location = r"C:\Users\srina\Music\Viva La Vida or Death And All Of His Friends\07. Viva La Vida.mp3"
song_location = r"C:\Users\srina\Music\A Rush Of Blood To The Head (2002)\03-coldplay-god_put_a_smile_upon_your_face.mp3"

chords = chordino.extract(song_location)


chord_list = []
times_list = []
for i in range(0,len(chords)):
    #print(i)
    chord_list.append(chords[i].chord)
    times_list.append(float("{:.3f}".format(chords[i].timestamp)))

#print(chord_list,"\n\n",times_list)
song_info = song_location.split("\\")[-1]
#print(song_info)
#for i in range(0,len(chords)):
#    print(f"Chord = {chord_list[i]}, at time {times_list[i]}.")
    
print()

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

    print(raw_chord, chord)
    
    is_minor = int(any(x=="m" for x in chord))
    if 'm' in chord:
        position_difference = scales.index(chord[:-1])
    else:
        position_difference = scales.index(chord)
    sequence = [ [1,1,0,0,0,1,0,1,0,0,0,0] , [0,1,0,1,0,0,0,0,1,0,1,0] ][is_minor]
    scale_array = cyclic_shift(sequence, position_difference)
    scales_used = array_add(scales_used, scale_array)

print(scales_used, max(scales_used), len(chord_list))
key_signature = scales_used.index(max(scales_used))
print(f"Key signature : {scales[key_signature]} (or {scales[(key_signature-3)%12]}m)")
print("\nEnd of computation!")
