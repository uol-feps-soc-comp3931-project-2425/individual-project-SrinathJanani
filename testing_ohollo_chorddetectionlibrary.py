from chord_extractor.extractors import Chordino

# Setup Chordino with one of several parameters that can be passed
chordino = Chordino(roll_on=1)  

# Optional, only if we need to extract from a file that isn't accepted by librosa
#song_location = r"C:\Users\srina\Music\morgan powers - Disarray.mp3"
song_location = r"C:\Users\srina\Music\Viva La Vida or Death And All Of His Friends\07. Viva La Vida.mp3"
#song_location = chordino.preprocess(r"C:\Users\srina\Music\Parachutes (2000)\01 Don't Panic.m4a")
#song_location = r"C:\Users\srina\Music\Minecraft_Volume_Beta[M]\20. Chirp.mp3"
#song_location = r"C:\Users\srina\Music\A Rush Of Blood To The Head (2002)\03-coldplay-god_put_a_smile_upon_your_face.mp3"

# Run extraction
chords = chordino.extract(song_location)
# => [  ChordChange(chord='N', timestamp=0.371519274), 
#       ChordChange(chord='C', timestamp=0.743038548), 
#       ChordChange(chord='Am7b5', timestamp=8.54494331),...]

chord_list = []
times_list = []
for i in range(0,len(chords)):
    #print(i)
    chord_list.append(chords[i].chord)
    times_list.append(float("{:.3f}".format(chords[i].timestamp)))

#print(chord_list,"\n\n",times_list)
song_name = song_location.split("\\")[-1]
print(song_name)
for i in range(0,len(chords)):
    print(f"Chord = {chord_list[i]}, at time {times_list[i]}.")
print("\nEnd of computation!")
