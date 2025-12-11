import praw
import time
import pandas as pd
from using_pushhift import Data
from dotenv import load_dotenv
import os

load_dotenv()
id = os.getenv("id")
secret = os.getenv("secret")

data = Data(amount=None, start_date="2024-01-01", end_date="2025-12-01", subreddit="MachineLearning")
all_ids, dicto = data.start_gathering()

reddit = praw.Reddit(
    client_id=id,
    client_secret=secret,
    user_agent="mybot by u/YOUR_REDDIT_USERNAME"
)
rows = []
for pid in all_ids:
    try:
        post = reddit.submission(id=pid)
        post.comments.replace_more(limit=0)
        comments = [c.body for c in post.comments.list()]
        if len(comments) < 5:
            print("Skipping low quality posts")
            continue
        title = dicto[pid][1] if post.title == "[deleted by user]" or post.title == "[ Removed by moderator ]" else post.title
        text = dicto[pid][0] if post.selftext == "[removed]" else post.selftext
        for c in comments:
            if c != "[removed]" and c != "[deleted]":
                rows.append({
                    "post_id": pid,
                    "subreddit": str(post.subreddit),
                    "score": post.score,
                    "title": title,
                    "text": text,
                    "comment": c
                })
        time.sleep(1)
    except Exception as e:
        print("Error:", pid, e)
df = pd.DataFrame(rows)
df.to_csv("tubitak-2209a-job-anxiety-ai/data gathering/askprogramming_data.csv", index=False)
