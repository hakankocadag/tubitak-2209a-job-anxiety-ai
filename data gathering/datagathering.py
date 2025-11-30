import praw
import time
from using_pushhift import Data
data = Data(amount=10, start_time="2024-01-01", subreddit="futurology")
all_ids = data.start_gathering()
reddit = praw.Reddit(
    client_id="o7sT31PL8hYRCKi-CsSTJw",
    client_secret="7ZFjTd6Zl2e999q-FoUB53qDZ1i4FA",
    user_agent="mybot by u/YOUR_REDDIT_USERNAME"
)
for pid in all_ids:
    try:
        print(f"[+] Fetching post {pid}")
        post = reddit.submission(id=pid)
        post.comments.replace_more(limit=0)
        comments = [c.body for c in post.comments.list()]
        print("Commments : ")
        for x in comments:
            print(x)
        print("TITLE:", post.title)
        print("TEXT:", post.selftext)
        print("COMMENTS:", len(comments))
        print("---")
        time.sleep(1)
    except Exception as e:
        print("[-] Error for", pid, ":", e)