import praw
import os

# Reddit API credentials
# Replace credentials with your Reddit API credentials
reddit = praw.Reddit(
    client_id='MY_CLIENT_ID',
    client_secret='MY_SECRET_KEY',
    user_agent='MY_USER_AGENT'
)

# Subreddit to scrape
subreddit = reddit.subreddit("VALORANT")

# Output folder to save the posts
# Change to "question_posts for question flair"
output_folder = "discussion_posts"     
os.makedirs(output_folder, exist_ok=True)

# Fetch posts with the 'Discussion' flair
# Adjust the limit as needed
# Change flair to Question for question posts
discussion_posts = subreddit.search("flair:Discussion", sort="new", limit=100)  

# Loop through posts and save each as a separate txt file
for idx, post in enumerate(discussion_posts, start=1):
    filename = f"{output_folder}/text{idx}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"{post.title}\n\n")
        file.write(f"{post.selftext}\n")
    print(f"Saved: {filename}")

print("All discussion posts have been saved.")
