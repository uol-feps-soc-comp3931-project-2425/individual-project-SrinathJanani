# Music Artist Classification Based on Chord Progressions

This project investigates whether chord progressions alone can be used to classify songs by their respective music artists. The goal was to determine if harmonic structure, independent of lyrics or audio features, contains enough stylistic information to allow machine learning algorithms to identify the artist of a given song.

### This project covered:
- The onstruction of a dataset of songs from popular artists, annotated with chord progressions.
- Data preprocessing of chords by simplifying complex chords, converting to a uniform notation and ordering chords for enumeration.
- The application and comparison of several supervised machine learning algorithms to classify songs by artist based on chord progressions alone.
- Evaluation of the feasibility and accuracy of this approach using baseline models and modifying various processing strategies.

### Repository Structure

- `database.csv` – The manually curated dataset containing song names and music artists, key signatures, and extracted chord progressions.
- `processing.py` – Contains all data preprocessing functions including chord simplification, key normalization, and Roman numeral conversion.
- `automated_chord_recognition.py` – Initial attempt at extracting chords from audio using Ohollo’s Chordino plugin (not used in final implementation due to accuracy issues).
- `extra_methods.py` – Contains additional functions and unused experiments tested during the project.
- `project_log.txt` – Document tracking the progress, milestones, and decisions taken during the development of the project.
- `README.md` – This file (currently blank).
- `main.py` or equivalent – The script(s) used to train and test machine learning models (to be added if applicable).

## Methods and Tools

- **Language:** Python 3.8  
- **Libraries:** `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`  
- **Models Used:** Decision Trees, k-Nearest Neighbours (k=1, 3, 5), Logistic Regression, Support Vector Machines  
- **Baseline:** Dummy Classifier (stratified random prediction)  
- **Data Representation:** Chords simplified to major/minor, converted to Roman numeral notation, and optionally enumerated for machine learning

## Results Summary

- Chord progressions alone achieved better-than-random classification in some models, with KNN and SVM outperforming the dummy classifier for most tests.
- The most effective configuration achieved an accuracy of 70.6% when classifying songs between two artists.
- Performance declined as the number of artists increased, highlighting the limitations of using only chord sequences for stylistic classification.
- Dataset limitations (manual size and genre homogeneity) were the primary constraints on model performance.

## Limitations and Future Work

- Expand the dataset using improved chord recognition or ethically verified scraping techniques.
- Integrate other features such as rhythm, lyrics, instrumentation, or key signature.
- Explore deep learning methods and ensemble approaches on a larger, more diverse dataset.
- Investigate chord progression patterns across genres and sub-genres.

## Acknowledgements

Supervised by Dr. Sebastian Ordyniak  
Project developed by Srinath Srikanth Janani  
University of Leeds – School of Computer Science, 2025
