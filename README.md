# Music Artist Classification Based on Chord Progressions

This project investigates whether chord progressions alone can be used to classify songs by their respective music artists. The goal was to determine if harmonic structure, independent of lyrics or audio features, contains enough stylistic information to allow machine learning algorithms to identify the artist of a given song.

### This project covered:
- The onstruction of a dataset of songs from popular artists, annotated with chord progressions.
- Data preprocessing of chords by simplifying complex chords, converting to a uniform notation and ordering chords for enumeration.
- The application and comparison of several supervised machine learning algorithms to classify songs by artist based on chord progressions alone.
- Evaluation of the feasibility and accuracy of this approach using baseline models and modifying various processing strategies.

### The files in this repository have the following functions:

- `song_database.py` – The manually curated dataset containing song names and music artists, key signatures, and extracted chord progressions, here being stored in python.
- `chord_utilizing_functions.py` - All methods and functions that were used for data preprocessing.
- `ML algorithms.py` - The python file which hosts the models training and testing on the data, as well as the evaluation of the results.
- `testing_ohollo_chorddetectionlibrary.py` - Scrapped method of attempting chord recognition to automate the database creation.
- `key_signature_detection.py` - Scrapped function which successfully estimates the key signature of a song given the chords.
- `key_detection_and_notation_conversion.py` - Scrapped file of data preprocessing techniques for the chord recognition method.
- `Progress Notes.txt` - Text file documenting the progress of the project and personal notes left regarding nuances and advances in the project.


### Methods and tools used here are:

- **Language:** Python 3.8  
- **Libraries:** `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`  
- **Models Used:** Decision Trees, k-Nearest Neighbours (k=1, 3, 5), Logistic Regression, Support Vector Machines (Linear Regression - scrapped)
- **Baseline:** Dummy Classifier (stratified random prediction)  
- **Data Representation:** Chords simplified to major/minor, converted to Roman numeral notation, and optionally enumerated for machine learning


### Results Summary

Chord progressions alone achieved better-than-random classification in some models, with KNN and SVM outperforming the dummy classifier for most tests. The most effective configurations achieved highest accuracy when classifying songs between two artists only. Performance declined as the number of artists increased, highlighting the limitations of using only chord sequences for stylistic classification. However if combined with other musical features, chord progressions may be a useful input feature in classifying music artists and in detecting musical style.


### Acknowledgements

Supervised by Dr. Sebastian Ordyniak  
Project developed by Srinath Srikanth Janani  
University of Leeds – School of Computer Science, 2025
