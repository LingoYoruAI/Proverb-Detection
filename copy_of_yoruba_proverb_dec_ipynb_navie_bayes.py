# -*- coding: utf-8 -*-
"""Copy of Yoruba Proverb_Dec.ipynb Navie bayes

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ea_PNJBTybWC5rOD--wFMcemxKulrWRa

# **Import** **Necessary** **Libraries**
"""

!pip install nltk pandas scikit-learn

import nltk
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from google.colab import drive
drive.mount('/content/drive')

"""## **Data** **Review**

**Load** **dataset**
"""

# Load the datasets
df1 = pd.read_csv('/content/drive/MyDrive/New_trainset_proverb - Sheet1 (1).csv')
df2 = pd.read_csv('/content/drive/MyDrive/Proverb_Dec_new -.csv')

df1 = df1.iloc[:, :2]
df2 = df2.iloc[:, :2]

df1.columns = ['Proverbs', 'Labels']
df2.columns = ['Proverbs', 'Labels']

# Concatenate the datasets
Proverbs_df = pd.concat([df1, df2], ignore_index=True)

# Save the combined dataset to a new CSV
Proverbs_df.to_csv('/content/drive/MyDrive/Proverbs_data.csv', index=False)

print("Datasets combined successfully and saved as 'Proverbs_data.csv'.")

# Check for the first 5 rows
Proverbs_df.head()

# Check for the last five rows
Proverbs_df.tail()

Proverbs_df.columns

Proverbs_df.info() # information about the data

"""**Descriptive statistics of the dataset**"""

Proverbs_df.describe()

"""**Shape** **of** **the** **dataset**"""

Proverbs_df.shape

"""Check for missing values using isnull()"""

Proverbs_df.isnull().sum()

"""There are no missing values in both Proverbs and labels columns."""

# Checking for duplicate rows in the DataFrame
Proverbs_df.duplicated().sum()

"""There are 74 rows in the DataFrame that are duplicates of other rows."""

# Clean up whitespace and casing
Proverbs_df['Proverbs'] = Proverbs_df['Proverbs'].str.strip().str.lower()

# Drop exact duplicates
Proverbs_df = Proverbs_df.drop_duplicates()

# Save the cleaned dataset to a new CSV file
Proverbs_df.to_csv('/content/drive/MyDrive/Cleaned_Combined_Proverbs.csv', index=False)

# Drop duplicates rows
data = Proverbs_df.drop_duplicates()

Proverbs_df.duplicated().sum()

# Check for the new data shape
Proverbs_df.shape

Proverbs_df.dtypes

# Check for unique values
Proverbs_df['Proverbs'].unique()

# Check for unique values in the label column
Proverbs_df['Labels'].unique()

"""* 1 = Proverb
* 0 = Non_Proverbs
"""

Proverbs_df['Labels'].value_counts()

"""* There are 7970 proverbs in the label column and 7962 non proverbs.

# **Data Visualization**

## Bar Plot
"""

# Check for distribution of proverbs and non-proverbs
sns.countplot(x='Labels', data=data, color='blue')
plt.title('Distribution of Proverbs vs Non-Proverbs')
plt.show()

"""## Pie Chart Plot"""

# Distribution between Proverbs and Non-Proverbs using Pie Chart
Proverbs_df['Labels'].value_counts().plot(kind='pie', autopct='%1.1f%%')

plt.title('Proverb vs Non-Proverb Proportions')
plt.show()

"""## Data Preprocessing

Text Normalization

* Lowering text.
* Tokenization .
* Stemming.
* Removal of stopwords.
* Removal of punctuation.

Vectorization
TF_IDF

## Text Normalization
"""

from transformers import BertTokenizer
import pandas as pd

# Load the combined dataset
data = pd.read_csv('/content/drive/MyDrive/Cleaned_Combined_Proverbs.csv')

# multilingual BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# Tokenize the 'Proverbs' column using subword tokenization
data['Proverbs'] = data['Proverbs'].apply(lambda x: tokenizer.tokenize(x))

# Save the tokenized dataset
data.to_csv('/content/drive/MyDrive/Subword_Tokenized_Proverbs.csv', index=False)

print("Subword tokenization complete! Saved as 'Subword_Tokenized_Proverbs.csv'.")

df = pd.read_csv('/content/drive/MyDrive/Subword_Tokenized_Proverbs.csv')

df.head()

df.tail()

def remove_punctuations(text):
    # Check if the input is a string
    if isinstance(text, str):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for x in text:
            if x in punctuations:
                text = text.replace(x, "")
        return text
    # If the input is a list
    elif isinstance(text, list):
        # Join the list elements into a string
        text_str = " ".join(text)
        # Apply the same logic as before on the joined string
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for x in text_str:
            if x in punctuations:
                text_str = text_str.replace(x, "")
        # Return the cleaned string
        return text_str
    # Handle cases where input is neither a string nor a list
    else:
        return text

data['Proverbs'] = data['Proverbs'].apply(remove_punctuations)
data.head()

"""* URL removal
* HTML tag removal
* Tokenization
* Stopword removal
* Stemming
"""

import re
from nltk.stem import PorterStemmer

# Custom Yoruba stopword list
yoruba_stopwords = ['ó', 'ní', 'ṣe', 'rẹ̀', 'tí', 'àwọn', 'sí', 'ni', 'náà',
                    'láti', 'kan', 'ti', 'ń', 'lọ', 'o', 'bí', 'padà', 'sì',
                    'wá', 'lè', 'wà', 'kí', 'púpọ̀', 'mi', 'wọ́n', 'pẹ̀lú',
                    'a', 'ṣùgbọ́n', 'fún', 'jẹ́', 'fẹ́', 'kò', 'jù', 'pé',
                    'é', 'gbogbo', 'inú', 'bẹ̀rẹ̀', 'jẹ', 'nítorí', 'nǹkan',
                    'sínú', 'yìí', 'ṣé', 'àti', 'í', 'máa', 'nígbà', 'mo',
                    'an', 'mọ̀', 'bá', 'kì', 'ńlá', 'ọ̀pọ̀lọpọ̀', 'ẹmọ́',
                    'wọn', 'òun']

stop_words = list(yoruba_stopwords)

# stemmer
stemmer = PorterStemmer()

# Define function to remove URLs, HTML tags, stopwords, and apply stemming

def clean_text(text):
    # Check if input is a list and join into a string if necessary
    if isinstance(text, list):
        text = ' '.join(text)
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Tokenize the text
    words = text.split()

    # Remove stopwords and apply stemming
    filtered_and_stemmed_words = [stemmer.stem(word) for word in words if word.lower() not in stop_words]

    # Join the filtered and stemmed words back into a sentence
    return ' '.join(filtered_and_stemmed_words)

# Apply the clean_text function to each row in the 'Proverbs' column
df['Proverbs'] = data['Proverbs'].apply(clean_text)

df.head()

# a new DataFrame to keep cleaned text and labels
final_data = data[['Proverbs', 'Labels']].copy()

# save the new dataset
final_data.to_csv('cleaned_proverbs_with_labels.csv', index=False)

# Output
print(data[['Proverbs', 'Labels']])  # print the  cleaned text and labels

df.columns # new column

df = pd.read_csv('/content/cleaned_proverbs_with_labels.csv') # load the new dataset

df.head()

X = df['Proverbs']  # Features
y = df['Labels']  # Labels
# The clean_text represent the proverbs

"""# **Text Vectorization using TF-IDF**"""

from sklearn.feature_extraction.text import TfidfVectorizer

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the cleaned text data
X_tfidf = tfidf_vectorizer.fit_transform(X)

# Convert the TF-IDF sparse matrix to a dense format
X_tfidf_dense = X_tfidf.toarray()

# Create a DataFrame with the feature names (terms)
tfidf_df = pd.DataFrame(X_tfidf_dense, columns=tfidf_vectorizer.get_feature_names_out())

# Display the DataFrame
print(tfidf_df)

"""# **Training and Evaluation Using Naive Bayes Model**"""

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Initialize the Naive Bayes classifier
nb_classifier = MultinomialNB()

# Train the model
nb_classifier.fit(X_train, y_train)

# Make predictions
y_pred = nb_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Classification Report:\n{report}')

from sklearn.metrics import confusion_matrix  # Import confusion_matrix

cm = confusion_matrix(y_test, y_pred)
print(cm)

# Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot heatmap
plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Negative", "Positive"], yticklabels=["Negative", "Positive"])
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix Heatmap")
plt.show()

#  predictions on the test set
test_predictions = nb_classifier.predict(X_test)

# Output of predictions along with the actual labels
for actual, predicted in zip(y_test, test_predictions):
    print(f'Actual Label: {actual} - Predicted Label: {predicted}')

# Example new data
new_data = ["Agba ki wa loja, ki ori omo titun o wo."]
# Transform the new data using the same TF-IDF vectorizer
new_data_tfidf = tfidf_vectorizer.transform(new_data)

# Make predictions on the new data
new_predictions = nb_classifier.predict(new_data_tfidf)

# Output of predictions along with the text
for text, predicted_label in zip(new_data, new_predictions):
    print(f'Text: "{text}" - Predicted Label: {predicted_label}')

true_labels = ["proverb"]

for text, actual, predicted in zip(new_data, true_labels, new_predictions):
    print(f'Text: "{text}" - Actual Label: {actual} - Predicted Label: {predicted}')

"""# **Save Model**"""

import joblib

# Save the trained Naive Bayes classifier and the TF-IDF vectorizer
joblib.dump(nb_classifier, 'naive_bayes_classifier.pkk')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkk')

