### ChatGPT imports
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score

# Libraries for data processing
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder          # Encoding music artists to integers
from sklearn.model_selection import train_test_split    # splitting data into training and testing

# Machine learning models:
from sklearn.tree import DecisionTreeClassifier         # Decision Trees
from sklearn.neighbors import KNeighborsClassifier      # k-Nearest Neighbours
from sklearn.linear_model import LogisticRegression     # Logistic Regression
from sklearn.svm import SVC                             # Support Vector Machine
from sklearn.linear_model import LinearRegression       # Linear Regression
from sklearn.dummy import DummyClassifier               # Dummy Classifier (for baseline)

### Importing of different algorithms


# Dummy Classifier
from sklearn.dummy import DummyClassifier

def ExecuteDummy(X_train, X_test, y_train, y_test):
    dummy_clf = DummyClassifier(strategy="stratified")
    dummy_clf.fit(X_train, y_train)
    y_dummy_pred = dummy_clf.predict(X_test)

    print("Dummy Classifier Accuracy:", accuracy_score(y_test, y_dummy_pred))
    print(classification_report(y_test, y_dummy_pred, zero_division = 1))

    return accuracy_score(y_test, y_dummy_pred)

# k Nearest Neighbours
from sklearn.neighbors import KNeighborsClassifier

def ExecuteKNN(X_train, X_test, y_train, y_test):
    for k in [1,3,5,8]:  # Various k values to test
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        print(f"kNN (k={k}) Accuracy: {accuracy_score(y_test, y_pred)}")
        print(classification_report(y_test, y_pred, zero_division = 1))
        print(confusion_matrix(y_test, y_pred))
        print("-" * 40)

    return accuracy_score(y_test, y_pred)


# Multinomial Logistic Regression (binary classification)
from sklearn.linear_model import LogisticRegression

def ExecuteLR(X_train, x_test, y_train, y_test):
    log_reg = LogisticRegression(max_iter = 500)
    log_reg.fit(X_train, y_train)
    y_pred = log_reg.predict(X_test)

    print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division = 1))
    print(confusion_matrix(y_test, y_pred))

    return accuracy_score(y_test, y_pred)

from sklearn.model_selection import train_test_split

# Linear Regression
from sklearn.linear_model import LinearRegression
from scipy import stats
#slope, intercept, r, p, std_err = stats.linregress(x, y)

def ExecuteLinReg(X_train, x_test, y_train, y_test):
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    y_pred = lin_reg.predict(X_test)

    # Convert regression output into class labels (0 or 1)
    y_pred = np.round(y_pred).astype(int)
    print("y-pred = ", y_pred)

    print("Linear Regression Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division = 1))
    print(confusion_matrix(y_test, y_pred))

    return accuracy_score(y_test, y_pred)



# Decision Trees
from sklearn import tree # not needed?
from sklearn.tree import DecisionTreeClassifier

def ExecuteDT(X_train, x_test, y_train, y_test):
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    y_pred = dt.predict(X_test)

    print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division = 1))
    print(confusion_matrix(y_test, y_pred))

    #VisualiseDT(dt)
    return accuracy_score(y_test, y_pred)


def VisualiseDT(clf):
    from sklearn.tree import export_graphviz
    from sklearn.externals.six import StringIO  
    from IPython.display import Image  
    import pydotplus

    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = feature_cols,class_names=['0','1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
    graph.write_png('diabetes.png')
    Image(graph.create_png())


# Support Vector Machine (uses SVC for multi-class instead of svm)
from sklearn.svm import SVC

def ExecuteSVM(X_train, x_test, y_train, y_test):
    svm = SVC(kernel='linear')
    svm.fit(X_train, y_train)
    y_pred = svm.predict(X_test)

    print("SVM Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division = 1))
    print(confusion_matrix(y_test, y_pred))

    return accuracy_score(y_test, y_pred)



### Imports from custom files

from song_database import database as raw_data

import chord_utilizing_functions as funcs


# Pre processing the data

processed_data = []
alt = 1
#processed_data_2

for i in raw_data[12*0:12*8]:
    
    data_row = i[:-1]
    key_sig = funcs.AccidentalsConversion(data_row[-1], 'b#')
    for point in i[-1]:
        
        chord_array = point
        enum_array = [] # enumerated values of chords w.r.t funcs.EnumerateChords
        enum_ordered_arr = []
        #print("> ", chord_array, key_sig)
        
        for i in range(0,len(chord_array)):
            chord_array[i] = funcs.CleanChord(chord_array[i],1)
        chord_array = funcs.ConvertToRoman(chord_array, key_sig)

        count = 0
        for chord in chord_array:
            enum_array.append( funcs.EnumerateChords.index(chord) )

            if count == 0:
                enum_ordered_arr.append( funcs.EnumerateChords.index(chord) )
            else:
                enum_ordered_arr.append( enum_array[-1] - enum_array[-2] )
            count += 1

        processed_data.append(data_row + [chord_array] + [enum_array] + [enum_ordered_arr])

# This processed the data into individual datapoints (progressions) set to a
# universal scale and enumerated according to frequency of chords


### Ordering the data fittable into training

ready_data = [[info[0],info[1],info[-2]] for info in processed_data]

df = pd.DataFrame(ready_data, columns=['Artist', 'Song', 'Chords'])
df[['C1', 'C2', 'C3', 'C4']] = pd.DataFrame(df['Chords'].tolist(), index=df.index)

df.drop(columns=['Chords'], inplace=True) # Removing label column

# Enumerating artists 
label_encoder = LabelEncoder()
df['Artist'] = label_encoder.fit_transform(df['Artist'])

X = df[['C1', 'C2', 'C3', 'C4']].values
y = df['Artist'].values

# Split into train (80%) and test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


### Training the models

out_arr = []

print(">>>")
out_arr.append(ExecuteDummy(X_train, X_test, y_train, y_test))
print(">>>")
out_arr.append(ExecuteKNN(X_train, X_test, y_train, y_test))
print(">>>")
out_arr.append(ExecuteLR(X_train, X_test, y_train, y_test))
print(">>>")
out_arr.append(ExecuteLinReg(X_train, X_test, y_train, y_test))
print(">>>")
out_arr.append(ExecuteDT(X_train, X_test, y_train, y_test))
print(">>>")
out_arr.append(ExecuteSVM(X_train, X_test, y_train, y_test))

label_counts = pd.Series(y_train).value_counts()

print(f"||| {out_arr} |||")

#print(label_counts)

### Model evaluations

models = {
    "kNN (k=3)": KNeighborsClassifier(n_neighbors=3),
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "SVM": SVC(kernel="linear"),
    "Linear Regression": LinearRegression()
}

'''
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5)  # 5-Fold Cross-Validation
    print(f"{name} Cross-Validation Accuracy: {scores.mean():.2f} ± {scores.std():.2f}")
'''

# Trying to print the data:

'''
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Reduce 4D to 2D
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Plot with class labels (Artist)
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='tab10', alpha=0.7)
plt.title("PCA - Chord Progressions Colored by Artist")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(scatter, label="Artist ID")
plt.grid(True)
plt.show()
'''

''' ###
import matplotlib.pyplot as plt
import numpy as np

# Setup
unique_labels = np.unique(y)
label_names = label_encoder.inverse_transform(unique_labels)
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))

# Create figure and axes
fig, axes = plt.subplots(1, 4, figsize=(18, 5))
scatter_plots = []

# Plot each pair
label_to_color = {label: colors[i] for i, label in enumerate(unique_labels)}

# C1 vs C2
for label in unique_labels:
    mask = y == label
    scatter = axes[0].scatter(df.loc[mask, 'C1'], df.loc[mask, 'C2'], 
                              color=label_to_color[label], label=label_names[label], alpha=0.7)
axes[0].set_title("C1 vs C2")
axes[0].set_xlabel("C1")
axes[0].set_ylabel("C2")

# C2 vs C3
for label in unique_labels:
    mask = y == label
    axes[1].scatter(df.loc[mask, 'C2'], df.loc[mask, 'C3'], 
                    color=label_to_color[label], label=label_names[label], alpha=0.7)
axes[1].set_title("C2 vs C3")
axes[1].set_xlabel("C2")
axes[1].set_ylabel("C3")

# C3 vs C4
for label in unique_labels:
    mask = y == label
    axes[2].scatter(df.loc[mask, 'C3'], df.loc[mask, 'C4'], 
                    color=label_to_color[label], label=label_names[label], alpha=0.7)
axes[2].set_title("C3 vs C4")
axes[2].set_xlabel("C3")
axes[2].set_ylabel("C4")

# C1 vs C4
for label in unique_labels:
    mask = y == label
    axes[3].scatter(df.loc[mask, 'C1'], df.loc[mask, 'C4'], 
                    color=label_to_color[label], label=label_names[label], alpha=0.7)
axes[3].set_title("Artists")
axes[3].set_xlabel("")
axes[3].set_ylabel("")
axes[3].legend()

# Create a shared legend (only once)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1.02, 0.5), title="Artists")

# Final layout
plt.suptitle("Chord Transitions by Artist", fontsize=16)
plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.show()

''' ###

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Setup
unique_labels = np.unique(y)
label_names = label_encoder.inverse_transform(unique_labels)
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))

# Create figure and axes
fig, axes = plt.subplots(1, 4, figsize=(18, 5))
scatter_plots = []

# Plot each pair
label_to_color = {label: colors[i] for i, label in enumerate(unique_labels)}

# Function to plot linear regression line
def plot_regression_line(ax, X, y, color, label):
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    ax.plot(X, y_pred, color=color, label=f"Regression: {label}")

# C1 vs C2
for label in unique_labels:
    mask = y == label
    scatter = axes[0].scatter(df.loc[mask, 'C1'], df.loc[mask, 'C2'], 
                              color=label_to_color[label], label=label_names[label], alpha=0.7)
    # Add linear regression line
    #plot_regression_line(axes[0], df.loc[mask, 'C1'].values.reshape(-1, 1), df.loc[mask, 'C2'].values, 
                         #label_to_color[label], label_names[label])
axes[0].set_title("C1 vs C2")
axes[0].set_xlabel("C1")
axes[0].set_ylabel("C2")

# C2 vs C3
for label in unique_labels:
    mask = y == label
    axes[1].scatter(df.loc[mask, 'C2'], df.loc[mask, 'C3'], 
                    color=label_to_color[label], label=label_names[label], alpha=0.7)
    # Add linear regression line
    #plot_regression_line(axes[1], df.loc[mask, 'C2'].values.reshape(-1, 1), df.loc[mask, 'C3'].values, 
                         #label_to_color[label], label_names[label])
axes[1].set_title("C2 vs C3")
axes[1].set_xlabel("C2")
axes[1].set_ylabel("C3")

# C3 vs C4
for label in unique_labels:
    mask = y == label
    axes[2].scatter(df.loc[mask, 'C3'], df.loc[mask, 'C4'], 
                    color=label_to_color[label], label=label_names[label], alpha=0.7)
    # Add linear regression line
    #plot_regression_line(axes[2], df.loc[mask, 'C3'].values.reshape(-1, 1), df.loc[mask, 'C4'].values, 
                         #label_to_color[label], label_names[label])
axes[2].set_title("C3 vs C4")
axes[2].set_xlabel("C3")
axes[2].set_ylabel("C4")

# C1 vs C4
for label in unique_labels:
    mask = y == label
    axes[3].scatter(df.loc[mask, 'C1'], df.loc[mask, 'C4'], 
                    color=label_to_color[label], label=label_names[label], alpha=0.7)
    # Add linear regression line
    #plot_regression_line(axes[3], df.loc[mask, 'C1'].values.reshape(-1, 1), df.loc[mask, 'C4'].values, 
                         #label_to_color[label], label_names[label])
axes[3].set_title("C1 vs C4")
axes[3].set_xlabel("")
axes[3].set_ylabel("")
axes[3].legend()

# Create a shared legend (only once)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1.02, 0.5), title="Artists")

# Final layout
plt.suptitle("Chord Transitions by Artist with Regression Lines", fontsize=16)
plt.tight_layout(rect=[0, 0, 0.9, 1])
#plt.show()






