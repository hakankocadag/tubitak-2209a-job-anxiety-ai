import praw
import time
import pandas as pd
import os
from dotenv import load_dotenv
from using_pushhift import Data
load_dotenv()
client_id = os.getenv("id")
client_secret = os.getenv("secret")
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="research_bot_v1.0_u_yourname"
)
data_gatherer = Data(amount=None, start_date="2024-01-01", end_date="2025-12-01", subreddit="jobs")
all_ids, dicto = data_gatherer.start_gathering()
rows = []
for pid in all_ids:
    try:
        post = reddit.submission(id=pid)
        post.comments.replace_more(limit=0)
        all_comments = post.comments.list()
        if len(all_comments) < 5:
            print("Skipping low quality posts")
            continue
        entry = dicto[pid]
        backup_text = entry['text'] if isinstance(entry, dict) else entry[0]
        backup_title = entry['title'] if isinstance(entry, dict) else entry[1]
        final_title = backup_title if post.title in ["[deleted by user]", "[ Removed by moderator ]"] else post.title
        final_text = backup_text if post.selftext in ["[removed]", "[deleted]"] else post.selftext
        for comment in all_comments:
            if comment.body in ["[removed]", "[deleted]"]:
                continue
            rows.append({
                "post_id": pid,
                "subreddit": str(post.subreddit),
                "score": post.score,
                "title": final_title,
                "text": final_text,
                "comment": comment.body,
            })
        print(f"Successfully processed post: {pid}")
        time.sleep(2)
    except Exception as e:
        if "401" in str(e):
            print(f"Auth Error: Check your client_id and secret. {e}")
            break
        print(f"Error processing {pid}: {e}")
if rows:
    df = pd.DataFrame(rows)
    output_file = "tubitak-2209a-job-anxiety-ai/data gathering/jobs_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSuccess! Saved {len(df)} rows to {output_file}")
else:
    print("\nNo data gathered. Check your keyword filters or comment count threshold.")