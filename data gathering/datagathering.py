import praw
import time
from using_pushhift import Data
from dotenv import load_dotenv
import os

load_dotenv()
id = os.getenv("id")
secret = os.getenv("secret")
data = Data(amount=10, start_date="2024-01-01", end_date="2025-12-01",subreddit="engineering")
all_ids, dicto = data.start_gathering()
reddit = praw.Reddit(
    client_id=id,
    client_secret=secret,
    user_agent="mybot by u/YOUR_REDDIT_USERNAME"
)
for pid in all_ids:
    try:
        print(f"[+] Fetching post {pid}")
        post = reddit.submission(id=pid)
        post.comments.replace_more(limit=0)
        comments = [c.body for c in post.comments.list()]
        if len(comments) < 10:
            print(f"[!] Skipping low quality post")
            continue
        print(f"[OK] Post {pid} has score {post.score}, printing details...")
        if post.title == "[deleted by user]":
            print("TITLE:", dicto[pid][1])
        else:
            print("TITLE:", post.title)
        if post.selftext == "[removed]":
            print("TEXT:", dicto[pid][0])
        else:
            print("TEXT:", post.selftext)
        print("Comments:")
        for x in comments:
            print(x)
        print("COMMENTS:", len(comments))
        print("---")
        time.sleep(1)
    except Exception as e:
        print("[-] Error for", pid, ":", e)
