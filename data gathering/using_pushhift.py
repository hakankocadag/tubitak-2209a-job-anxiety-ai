import requests
import datetime
class Data:
    def __init__(self, amount, start_time, subreddit):
        self.amount = amount                     
        self.start_time_str = start_time         
        self.subreddit = subreddit
        self.all_ids = []
        self.current_before = self.ts(self.start_time_str)
        self.job_keywords = [
            "job", "career", "work", "hiring", "employment",
            "laid off", "layoff", "salary", "profession"
        ]
        self.ai_keywords = [
    "ai", "artificial intelligence", "machine learning", "ml",
    "deep learning", "gpt", "chatgpt", "llm", "gemini",
    "claude", "midjourney", "dalle", "bard", "copilot",
        ]
        self.anxiety_keywords = [
    "afraid", "scared", "worried", "anxious",
    "fear", "fearful", "terrified", "panic",
    "worried about", "concerned", "job loss", 
    "lose my job", "replace me", "replacing us",
    "obsolete", "redundant", "layoff", "laid off"
    ]
        self.critical_phrases = [
    "ai replace", "ai replacing", "ai take my job",
    "ai taking jobs", "automation replace", 
    "automation replacing", "automation taking",
    "my job feel unsafe", "threatened by ai",
    "ai job loss", "fear ai"]
        self.exclude_keywords = [
    "how it work", "how does it work", "how something work",
    "does it work", "work well", "work properly", "work of",
    "work by", "work like", "work as a",
    "my first video", "tutorial", "explaining how", "animation",
    "youtube channel", "check out my", "subscribe", "like and share",
    "project", "made this", "built this", "tool i made"
]
    def ts(self, date_str):
        return int(datetime.datetime.strptime(date_str, "%Y-%m-%d").timestamp())
    def match_keywords(self, text):
        text = text.lower()
        job_hit = any(k in text for k in self.job_keywords)
        ai_hit  = any(k in text for k in self.ai_keywords)
        exclude_hit = any(bad in text for bad in self.exclude_keywords)
        return job_hit and ai_hit and (not exclude_hit)
    def start_gathering(self):
        while True:
            url = (
                "https://api.pullpush.io/reddit/search/submission/"
                f"?subreddit={self.subreddit}&before={self.current_before}&size=500"
            )
            response = requests.get(url).json()
            data = response.get("data", [])
            if not data:
                print("No more posts found. Stopping.")
                break
            for post in data:
                text = (post.get("title", "") + post.get("text", "")).lower()
                if self.match_keywords(text):
                    self.all_ids.append(post["id"])
            self.current_before = data[-1]["created_utc"]
            print("Total matching posts:", len(self.all_ids))
            if len(self.all_ids) >= self.amount:
                break
        return list(set(self.all_ids))
