# Importing the required libraries
import requests
import zipfile
import os
import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np

# URL of the ZIP file
url = 'https://github.com/krishnapriya-n/analysis-of-valorant-reddit-posts/Building and Analyzing Corpus/valorant_reddit.zip'
output_file = 'valorant_reddit.zip'

# Download the file using requests with error handling
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print("Download successful!")
except requests.exceptions.RequestException as e:
    print(f"Error downloading the file: {e}")

# Extract the ZIP file
corpus_folder = 'valorant_corpus'
if not os.path.exists(corpus_folder):
    with zipfile.ZipFile(output_file, 'r') as zip_ref:
        zip_ref.extractall(corpus_folder)
    print("Extraction successful!")
else:
    print("Corpus folder already exists.")

# List and validate extracted .txt files
extracted_files = [file for file in os.listdir(corpus_folder) if file.endswith(".txt")]

if extracted_files:
    print(f"Found {len(extracted_files)} text files.")
else:
    print("No text files found in the corpus folder. Please check the extraction process.")

# Initialize a dictionary to store the texts
corpus_texts = {}

# Read each .txt file dynamically
for filename in extracted_files:
    file_path = os.path.join(corpus_folder, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            corpus_texts[filename] = file.read()
    except IOError as e:
        print(f"Error reading {filename}: {e}")

# Verify successful reading of the corpus
if corpus_texts:
    print(f"\nSuccessfully loaded {len(corpus_texts)} files into the corpus dictionary.")
else:
    print("\nNo files were loaded. Please check for errors.")

# Create an NLTK corpus from the extracted .txt files
corpus = PlaintextCorpusReader(corpus_folder, r'.*\.txt')

# Print sample content from the first file to confirm readability
sample_file = corpus.fileids()[0]
print(f"\nContent of {sample_file} (first 50 characters):\n", corpus.raw(sample_file)[:50])

# Function to compute tokens and types for a single text
def get_tokens_and_types(text):
    tokens = corpus.words(text)  # Get the tokens for the text
    types = set(tokens)          # Get unique words (types)
    return tokens, types

# 1. Total tokens and types in the entire corpus
all_tokens = corpus.words()
all_types = set(all_tokens)

# 2. Total tokens and types for each text
text_metrics = {}
for file_id in corpus.fileids():
    tokens, types = get_tokens_and_types(file_id)
    text_metrics[file_id] = {
        'tokens': len(tokens),
        'types': len(types)
    }

# 3. Average number of tokens and types across all texts
total_tokens = sum([metrics['tokens'] for metrics in text_metrics.values()])
total_types = sum([metrics['types'] for metrics in text_metrics.values()])
num_texts = len(text_metrics)

avg_tokens = total_tokens / num_texts
avg_types = total_types / num_texts

# 4. Lexical diversity of the entire corpus
lexical_diversity = len(all_types) / len(all_tokens)

# Print the results
print(f"Total tokens in the entire corpus: {len(all_tokens)}")
print(f"Total types in the entire corpus: {len(all_types)}\n")

print("Tokens and Types for each text:")
for file_id, metrics in text_metrics.items():
    print(f"{file_id}: Tokens = {metrics['tokens']}, Types = {metrics['types']}")

print(f"\nAverage number of tokens per text: {avg_tokens:.2f}")
print(f"Average number of types per text: {avg_types:.2f}")
print(f"Lexical diversity of the entire corpus: {lexical_diversity:.4f}")

# Frequency distribution of all tokens in the entire corpus
all_tokens = corpus.words()
all_token_fd = FreqDist(all_tokens)

# Frequency distribution of types (unique words) in the entire corpus
all_types = set(all_tokens)
all_type_fd = FreqDist(all_types)

# Print the 10 most common tokens in the entire corpus
print("10 Most Common Tokens in the Corpus:")
print(all_token_fd.most_common(10))

# Print the 10 most common types (unique words) in the entire corpus
print("\n10 Most Common Types in the Corpus:")
print(all_type_fd.most_common(10))

# Frequency distribution for each text
text_frequency_distributions = {}
for file_id in corpus.fileids():
    text_tokens = corpus.words(file_id)
    text_fd = FreqDist(text_tokens)
    text_frequency_distributions[file_id] = text_fd

    # Print 5 most common words in the current text
    print(f"\n5 Most Common Words in {file_id}:")
    print(text_fd.most_common(5))

# Identify infrequent words (words that occur only once)
infrequent_words = [word for word, freq in all_token_fd.items() if freq == 1]
print("\nInfrequent Words (appear only once across the entire corpus):")
print(infrequent_words[:10])  # Display first 10 infrequent words

stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in all_tokens if word.lower() not in stop_words]

min_freq = 3
filtered_tokens = [word for word, freq in all_token_fd.items() if freq >= min_freq]

lowercased_tokens = [word.lower() for word in all_tokens]

from spellchecker import SpellChecker
spell = SpellChecker()
corrected_tokens = [spell.correction(word) for word in all_tokens]

stop_words = set(stopwords.words('english'))

# Dictionaries to store results
text_lexical_diversity = {}
filtered_lexical_diversity = {}

# Calculate TTR with and without stopwords
for file_id in corpus.fileids():
    tokens = [word.lower() for word in corpus.words(file_id) if word.isalpha()]
    
    # Overall TTR
    types = set(tokens)
    lexical_diversity_text = len(types) / len(tokens) if tokens else 0
    text_lexical_diversity[file_id] = lexical_diversity_text
    
    # TTR excluding stopwords
    content_tokens = [word for word in tokens if word not in stop_words]
    filtered_types = set(content_tokens)
    lexical_diversity_filtered = len(filtered_types) / len(content_tokens) if content_tokens else 0
    filtered_lexical_diversity[file_id] = lexical_diversity_filtered

# Print the overall TTR
print("\nOverall Lexical Diversity for Each Text:")
for file_id, diversity in text_lexical_diversity.items():
    print(f"{file_id}: Lexical Diversity = {diversity:.4f}")

# Print the filtered TTR (without stopwords)
print("\nFiltered Lexical Diversity (without stopwords) for Each Text:")
for file_id, diversity in filtered_lexical_diversity.items():
    print(f"{file_id}: Filtered Lexical Diversity = {diversity:.4f}")

# Convert data to percentages and get word counts
texts = list(text_lexical_diversity.keys())
overall_diversities = [val * 100 for val in text_lexical_diversity.values()]  # Overall TTR in %
filtered_diversities = [val * 100 for val in filtered_lexical_diversity.values()]  # Filtered TTR in %
word_counts = [len(corpus.words(file_id)) for file_id in corpus.fileids()]  # Total words in each text

# Define bar width and positions
bar_width = 0.3
index = np.arange(len(texts))

# Create the plot
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plot lexical diversities
ax1.bar(index, overall_diversities, bar_width, label='Overall Lexical Diversity (%)', color='#4E79A7')
ax1.bar(index + bar_width, filtered_diversities, bar_width, label='Filtered Lexical Diversity (%)', color='#F28E2B')

# Add labels and title for the first y-axis
ax1.set_xlabel('Text', fontsize=12)
ax1.set_ylabel('Lexical Diversity (%)', fontsize=12, color='black')
ax1.set_title('Lexical Diversity (Overall vs. Filtered) and Word Count for Each Text', fontsize=14)
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels(texts, rotation=45, ha='right')

# Display values on top of lexical diversity bars
for i, (overall, filtered) in enumerate(zip(overall_diversities, filtered_diversities)):
    ax1.text(i, overall + 1, f'{overall:.1f}%', ha='center', va='bottom', fontsize=10)
    ax1.text(i + bar_width, filtered + 1, f'{filtered:.1f}%', ha='center', va='bottom', fontsize=10)

# Create a second y-axis for word count
ax2 = ax1.twinx()
ax2.bar(index + 2 * bar_width, word_counts, bar_width, label='Total Words', color='#59A14F', alpha=0.7)
ax2.set_ylabel('Total Words', fontsize=12, color='black')

# Display values on top of word count bars
for i, count in enumerate(word_counts):
    ax2.text(i + 2 * bar_width, count + 10, f'{count}', ha='center', va='bottom', fontsize=10)

# Add combined legend
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95), fontsize=10)

# Add grid lines for better readability
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust layout to prevent overlap
fig.tight_layout()

# Display the plot
plt.show()