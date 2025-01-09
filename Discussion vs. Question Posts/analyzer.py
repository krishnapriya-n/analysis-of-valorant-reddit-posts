# Importing the required libraries
import requests
import os
import zipfile
import string
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# URLs of the ZIP files
urls = {
    "discussion_posts": "https://github.com/krishnapriya-n/valorant-reddit/raw/main/discussion_posts.zip",
    "question_posts": "https://github.com/krishnapriya-n/valorant-reddit/raw/main/question_posts.zip"
}

# Download and extract each ZIP file
for category, url in urls.items():
    output_file = f"{category}.zip"
    folder_name = category

    # Download the file with error handling
    try:
        print(f"Downloading {category}...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"Download successful: {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {category}: {e}")
        continue

    # Extract the ZIP file
    if not os.path.exists(folder_name):
        with zipfile.ZipFile(output_file, 'r') as zip_ref:
            zip_ref.extractall(folder_name)
        print(f"Extraction successful: {folder_name}")
    else:
        print(f"{folder_name} folder already exists.")

# Function to process text by tokenizing and removing punctuation
def process_text(text):
    """Tokenizes the text, removing punctuation and converting to lowercase."""
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).lower().split()

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def process_text(text):
    tokens = text.translate(str.maketrans('', '', string.punctuation)).lower().split()
    return [word for word in tokens if word not in stop_words]

# Function to analyze the corpus and calculate basic metrics
def analyze_corpus(folder):
    """Analyzes the corpus by calculating basic metrics."""
    total_texts = 0
    total_tokens = 0
    token_counter = Counter()

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            total_texts += 1
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                text = file.read()
                tokens = process_text(text)
                total_tokens += len(tokens)
                token_counter.update(tokens)

    total_types = len(token_counter)
    avg_words_per_text = total_tokens / total_texts if total_texts > 0 else 0
    ttr = total_types / total_tokens if total_tokens > 0 else 0

    return {
        "Total Texts": total_texts,
        "Total Tokens": total_tokens,
        "Total Types": total_types,
        "Average Words per Text": avg_words_per_text,
        "Type-Token Ratio": ttr
    }

# Analyze Discussion Posts
discussion_folder = "discussion_posts"
print("\nDiscussion Posts Metrics:")
if os.path.exists(discussion_folder):
    discussion_metrics = analyze_corpus(discussion_folder)
    for k, v in discussion_metrics.items():
        print(f"{k}: {v}")
else:
    print("Discussion folder not found.")

# Analyze Question Posts
question_folder = "question_posts"
print("\nQuestion Posts Metrics:")
if os.path.exists(question_folder):
    question_metrics = analyze_corpus(question_folder)
    for k, v in question_metrics.items():
        print(f"{k}: {v}")
else:
    print("Question folder not found.")

import nltk
from nltk.probability import FreqDist

# Get word frequencies for Discussion Posts
discussion_words = []
for filename in os.listdir(discussion_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(discussion_folder, filename), "r", encoding="utf-8") as file:
            discussion_words.extend(process_text(file.read()))

discussion_freq = FreqDist(discussion_words)
print("\nTop 20 words in Discussion Posts:")
print(discussion_freq.most_common(20))

# Get word frequencies for Question Posts
question_words = []
for filename in os.listdir(question_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(question_folder, filename), "r", encoding="utf-8") as file:
            question_words.extend(process_text(file.read()))

question_freq = FreqDist(question_words)
print("\nTop 20 words in Question Posts:")
print(question_freq.most_common(20))

# Generate and display word cloud for Discussion Posts
discussion_wordcloud = WordCloud(width=800, height=400).generate(" ".join(discussion_words))
plt.figure(figsize=(10, 5))
plt.imshow(discussion_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Discussion Posts Word Cloud")
plt.show()

# Generate and display word cloud for Question Posts
question_wordcloud = WordCloud(width=800, height=400).generate(" ".join(question_words))
plt.figure(figsize=(10, 5))
plt.imshow(question_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Question Posts Word Cloud")
plt.show()

def analyze_sentence_length(folder):
    total_sentences = 0
    total_words = 0

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                text = file.read()
                sentences = re.split(r'[.!?]', text)
                sentences = [s.strip() for s in sentences if s.strip()]
                total_sentences += len(sentences)
                total_words += sum(len(process_text(sentence)) for sentence in sentences)

    avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
    return avg_sentence_length

# Calculate for Discussion Posts
discussion_avg_sentence_length = analyze_sentence_length(discussion_folder)
print(f"Average Sentence Length (Discussion Posts): {discussion_avg_sentence_length:.2f}")

# Calculate for Question Posts
question_avg_sentence_length = analyze_sentence_length(question_folder)
print(f"Average Sentence Length (Question Posts): {question_avg_sentence_length:.2f}")

categories = ["Discussion", "Question"]
total_tokens = [discussion_metrics["Total Tokens"], question_metrics["Total Tokens"]]
avg_words = [discussion_metrics["Average Words per Text"], question_metrics["Average Words per Text"]]
ttr = [discussion_metrics["Type-Token Ratio"], question_metrics["Type-Token Ratio"]]

# Plot Total Tokens
plt.figure(figsize=(8, 5))
plt.bar(categories, total_tokens, color=['skyblue', 'lightgreen'])
plt.title("Total Tokens in Each Category")
plt.ylabel("Number of Tokens")
plt.show()

# Plot Average Words per Text
plt.figure(figsize=(8, 5))
plt.bar(categories, avg_words, color=['skyblue', 'lightgreen'])
plt.title("Average Words per Text")
plt.ylabel("Average Words")
plt.show()

# Plot Type-Token Ratio
plt.figure(figsize=(8, 5))
plt.bar(categories, ttr, color=['skyblue', 'lightgreen'])
plt.title("Type-Token Ratio Comparison")
plt.ylabel("TTR")
plt.show()
