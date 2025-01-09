# Importing required libraries
import praw
import os
import re
import csv

# Reddit API credentials
# Replace credentials with your Reddit API credentials
reddit = praw.Reddit(
    client_id='TOPSECRET',
    client_secret='TOPSECRET',
    user_agent='TOPSECRET'
)

# Subreddit to scrape
subreddit = reddit.subreddit("VALORANT")

# Output folder to save the posts
output_folder = "Corpus"
os.makedirs(output_folder, exist_ok=True)

# Define number of posts to collect per flair
posts_per_flair = 30

# Get a set of unique flairs in the subreddit
flairs = set()

def collect_unique_flairs(subreddit, limit=100):
    """
    Collects unique flairs from the given subreddit by fetching a set number of new posts.
    
    Args:
    - subreddit: The Reddit subreddit object to scrape posts from.
    - limit: The number of posts to inspect for unique flairs (default is 100).
    
    Returns:
    - A set of unique flairs found in the subreddit.
    """
    unique_flairs = set()
    for post in subreddit.new(limit=limit):
        if post.link_flair_text:
            unique_flairs.add(post.link_flair_text)
    return unique_flairs

def save_posts_to_csv(flair, posts):
    """
    Saves a list of posts related to a specific flair into a CSV file.

    Args:
    - flair: The flair/category for the current set of posts.
    - posts: The list of Reddit posts to save (each post is a PRAW submission object).
    
    The function creates a folder named after the flair and writes the post data into a CSV file.
    """
    # Create a folder for each flair within the Corpus directory
    flair_folder = os.path.join(output_folder, flair)
    os.makedirs(flair_folder, exist_ok=True)

    # Define the CSV file name for this flair
    csv_filename = os.path.join(flair_folder, f"{flair}_posts.csv")

    # Open the CSV file for writing (with headers)
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post ID', 'Title', 'Post Content', 'Upvotes', 'Comments'])  # Header row

        # Loop through posts and write each one to the CSV file
        for idx, post in enumerate(posts, start=1):
            writer.writerow([
                post.id,
                post.title,
                post.selftext.replace("\n", " "),  # Remove newlines from post content for CSV format
                post.score,
                post.num_comments
            ])
            print(f"Saved: {csv_filename} - Post {idx}")

def fetch_posts_by_flair(flair, limit=posts_per_flair):
    """
    Fetches a set number of posts from the subreddit with a specific flair.
    
    Args:
    - flair: The flair/category to filter the posts.
    - limit: The number of posts to fetch (default is 30).
    
    Returns:
    - A list of PRAW post objects with the specified flair.
    """
    return list(subreddit.search(f'flair:"{flair}"', sort="new", limit=limit))

# Main execution flow
if __name__ == "__main__":
    # Step 1: Collect unique flairs from the subreddit
    flairs = collect_unique_flairs(subreddit)

    # Step 2: Fetch posts for each flair and save them to CSV
    for flair in flairs:
        # Fetch posts with the current flair
        posts = fetch_posts_by_flair(flair)
        
        # Save posts to CSV
        save_posts_to_csv(flair, posts)

    print("All posts have been saved in their respective flair folders in CSV format.")
