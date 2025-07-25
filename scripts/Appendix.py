#Appendix

# -*- coding: utf-8 -*-
"""Final_A2.ipynb
Automatically generated by Colab.
Original file is located at
https://colab.research.google.com/drive/1bj57xDsH25RDEIMGyhIjWYOjLOil2qan
"""
# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import html
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# Download necessary NLTK datasets
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Importing the libraries
from google.colab import drive
import pandas as pd

# Mounting Google Drive
drive.mount('/content/drive')

# Specify the path
file_path = '/content/drive/My
Drive/Assignment/A_II_Emotion_Data_Student_Copy_Final.xlsx'

# Load the data
data = pd.read_excel(file_path)

# Displaying the first few rows of the data
print(data.head())

# Dictionary for contraction expansion
contractions_dict = {
"can't": "cannot",
"won't": "will not",
"n't": " not",
"'re": " are",
"'s": " is",
"'d": " would",
"'ll": " will",
"'t": " not",
"'ve": " have",
"'m": " am"
}

# Regex pattern for finding contractions
contractions_pattern =
re.compile('({})'.format('|'.join(contractions_dict.keys())),
flags=re.IGNORECASE|re.DOTALL)

# Function to expand contractions
def expand_contractions(text, contractions_dict=contractions_dict):
def replace(match):
return contractions_dict.get(match.group(0).lower(), match.group(0))
return contractions_pattern.sub(replace, text)

# Function to remove HTML tags
def clean_html(text):
return re.sub(r'<.*?>', '', html.unescape(text))

# Setup for text cleaning
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Main function to preprocess text
def clean_text(text):
if not text:
return ""
text = clean_html(text)
text = expand_contractions(text)
text = text.lower()
tokens = word_tokenize(text)
clean_tokens = [lemmatizer.lemmatize(word) for word in tokens if
word.isalpha() and word not in stop_words]
return ' '.join(clean_tokens)

# Clean and preprocess text data
data['cleaned_text'] = data['text_reviews_'].apply(clean_text)
#1. Box Plots for Star Ratings by Brand
def plot_count_star_ratings_by_brand():
plt.figure(figsize=(14, 8))
sns.countplot(x='brand_name_', hue='star_rating_', data=data,
palette='coolwarm')
plt.title('Count of Star Ratings by Brand')
plt.xticks(rotation=45)
plt.xlabel('Brand')
plt.ylabel('Count of Ratings')
plt.legend(title='Star Rating')
plt.show()
plot_count_star_ratings_by_brand()

#2. Count of Emotions
filtered_data = data[data['emotions_'] != 'unlabeled']
plt.figure(figsize=(8, 6))
sns.countplot(y='emotions_', data=filtered_data,
order=filtered_data['emotions_'].value_counts().index, palette='coolwarm')
plt.title('Count of Emotions')
plt.xlabel('Count')
plt.ylabel('Emotions')
plt.show()

#3. Brand Distribution
plt.figure(figsize=(8, 6))
data['brand_name_'].value_counts().plot(kind='pie', autopct='%1.1f%%',
startangle=90, colors=['skyblue', 'orange'])
plt.ylabel('') # To remove the y-label
plt.title('Brand Distribution')
plt.show()

#4. Top 10 Countries Distribution
top_countries = data['country_'].value_counts().head(10)
plt.figure(figsize=(10, 6))
top_countries.plot(kind='bar', color='purple')
plt.title('Top 10 Countries Distribution')
plt.xlabel('Country')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Sentiment analysis
def analyze_sentiment(text):
return TextBlob(text).sentiment.polarity
data['sentiment_polarity'] = data['cleaned_text'].apply(analyze_sentiment)
data['sentiment_classification'] = data['sentiment_polarity'].apply(lambda
x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral')

# Encode labels
label_encoder = LabelEncoder()
11
data['encoded_labels'] =
label_encoder.fit_transform(data['emotions_'].fillna('unlabeled'))

# Prepare label info for classification report
labels = np.unique(data['encoded_labels'])
target_names = label_encoder.inverse_transform(labels)

# Select features and labels for model training
supervised_data = data[data['emotions_'].notna()]
X = supervised_data['cleaned_text']
y = supervised_data['encoded_labels']
vectorizer = TfidfVectorizer(max_features=3000, stop_words='english',
ngram_range=(1,2))
X_vectorized = vectorizer.fit_transform(X)

# Feature selection using chi-squared test
chi2_selector = SelectKBest(chi2, k=2500)
X_chi2_selected = chi2_selector.fit_transform(X_vectorized, y)

# Stratified splitting of the dataset
X_train, X_test, y_train, y_test = train_test_split(X_chi2_selected, y,
test_size=0.3, random_state=42, stratify=y)

# Initialize logistic regression model Before Tuning
logistic_model = LogisticRegression(max_iter=10000, class_weight='balanced')

# Train the logistic regression model
logistic_model.fit(X_train, y_train)

#Evaluate the logistic regression model
predictions = logistic_model.predict(X_test)
print("Before tuning:")
print(classification_report(y_test, predictions, labels=labels,
target_names=target_names, zero_division=1))

# Accuracy
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

# Hyperparameter Tuning
param_grid = {'C': [0.01, 0.1, 1, 10], 'penalty': ['l1', 'l2'], 'solver':
['liblinear']}
grid_search = GridSearchCV(LogisticRegression(max_iter=10000,
class_weight='balanced'), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# After Tuning
predictions = best_model.predict(X_test)
print("After tuning:")
print(classification_report(y_test, predictions, labels=labels,
target_names=target_names, zero_division=1))

# Accuracy
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

# Prepare the data for emotion classification
data['emotions_'] = data['emotions_'].fillna('unlabeled')
label_encoder = LabelEncoder()
data['encoded_labels'] = label_encoder.fit_transform(data['emotions_'])

# Select features and labels for model training
supervised_data = data[data['emotions_'] != 'unlabeled']
X = supervised_data['cleaned_text']
y = supervised_data['encoded_labels']
vectorizer = TfidfVectorizer(max_features=3000, stop_words='english',
ngram_range=(1,2))
X_vectorized = vectorizer.fit_transform(X)

# Training the logistic regression model
logistic_model = LogisticRegression(max_iter=10000)
logistic_model.fit(X_vectorized, y)

# Predicting emotions for the entire dataset
all_data_vectorized = vectorizer.transform(data['cleaned_text'])
predicted_labels = logistic_model.predict(all_data_vectorized)
data['predicted_emotions'] =
label_encoder.inverse_transform(predicted_labels)

#Visual analytics
# Import libraries
import matplotlib.pyplot as plt
import seaborn as sns

#1. Distribution of Predicted Emotions by Brand
def plot_clustered_emotions(column, title):
plt.figure(figsize=(14, 8))
emotion_counts =
data.groupby('brand_name_')[column].value_counts(normalize=True).unstack().f
illna(0)
colors = sns.color_palette('muted',
n_colors=len(emotion_counts.columns))

# Plotting the data with the colors
emotion_counts.plot(kind='bar', color=colors, subplots=False)
plt.title(title)
plt.legend(title='Emotion', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.ylabel('Percentage')
plt.show()
plot_clustered_emotions('predicted_emotions', 'Distribution of Predicted
Emotions by Brand')

#2. Average Star Ratings by Brand
# Calculating average star rating per brand
brand_ratings =
data.groupby('brand_name_')['star_rating_'].mean().reset_index()

# Sort the data for better visualization
brand_ratings = brand_ratings.sort_values('star_rating_', ascending=False)
plt.figure(figsize=(12, 8))
sns.barplot(x='star_rating_', y='brand_name_', data=brand_ratings,
palette='viridis')
plt.title('Average Star Ratings by Brand')
plt.xlabel('Average Star Rating')
plt.ylabel('brand_name_')
plt.show()

#3. Distribution of Sentiment Classification
def plot_categorical(column, title, palette='deep'):
plt.figure(figsize=(10, 6))
ax = sns.countplot(y=column, data=data,
order=data[column].value_counts().index, palette=palette)
plt.title(title)
# Add data labels to each bar
for p in ax.patches:
ax.annotate(f'{int(p.get_width())}',
(p.get_width(), p.get_y() + p.get_height() / 2),
xytext=(5, 0),
textcoords='offset points',
ha='left',
va='center')
plt.show()
plot_categorical('sentiment_classification', 'Distribution of Sentiment
Classification', palette='muted')

#4. Distribution of Predicted Emotions
def plot_categorical(column, title, palette):
plt.figure(figsize=(10, 6))
sns.countplot(x=column, data=data,
order=data[column].value_counts().index, palette=palette)
plt.title(title)
plt.xticks(rotation=45)
plt.show()
palette = 'muted'
plot_categorical('predicted_emotions', 'Distribution of Predicted Emotions',
palette)

# Save the processed data to CSV file on Google Drive
output_path = '/content/drive/My Drive/Assignment/A2_output_final.csv'
data.to_csv(output_path, index=False)