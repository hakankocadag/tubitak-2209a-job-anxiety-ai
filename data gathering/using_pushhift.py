import requests
import datetime
import re
class Data:
    def __init__(self, amount, start_date, end_date, subreddit):
        self.amount = amount
        self.subreddit = subreddit
        self.start_ts = self.ts(start_date)
        self.end_ts = self.ts(end_date)
        self.current_before = self.end_ts
        self.all_ids = []
        self.job_keywords = [
            "job", "jobs", "career", "careers", "employment", "employed",
            "unemployment", "layoff", "laid off", "hiring",
            "job market", "workplace", "workforce", "working", "works", "worked", "replace", "replaces",
            "replaced", "replacing"
        ]
        self.ai_keywords = [
            "AI", "Artificial Intelligence", "GPT", "ChatGPT", "Claude", "LLM", "LLMS",
            "Bing", "LLAMA", "Midjourney", "DALL-E", "generative AI", "Gemini",
            "Copilot", "Perplexity AI", "Canva", "DeepL", "QuillBot", "Grammarly",
            "Character.ai", "Zapier", "Microsoft Copilot", "CapCut", "DeepAI",
            "Hugging Face", "Poe", "Suno", "ElevenLabs", "InVideo", "Leonardo",
            "Replit", "Consensus", "Runway", "Luma AI", "Filmora", "Otter.ai",
            "DeepSeek", "Stable Diffusion", "Grok", "Microsoft Designer", "you.com",
            "Synthesia", "Descript", "HeyGen", "Jasper", "OpusClip", "Play.ht",
            "Cursor", "Wordtune", "WriteSonic", "Copy.ai", "Murf.ai", "Pictory", "Pi",
            "Google AI Studio", "Krisp", "Fliki", "SlidesAI", "NotebookLM", "Groq",
            "Lumen5", "Rytr", "HyperWrite", "Resemble", "Tabnine", "Mem"
        ]

        self.exclude_keywords = [
            "benchmark", "latency", "performance", "release",
            "training", "parameters", "architecture", "vision capability",
            "model comparison", "openai update", "tutorial", "youtube channel",
            "animation", "subscribe", "check out my", "made this", "built this",
            "explaining how", "how it work", "work well", "work properly"
        ]
    def ts(self, s):
        return int(datetime.datetime.strptime(s, "%Y-%m-%d").timestamp())
    def match_keywords(self, text):
        t = text.lower()
        def word_hit(keywords):
            return any(re.search(rf"\b{re.escape(k.lower())}\b", t) for k in keywords)
        job_hit = word_hit(self.job_keywords)
        ai_hit = word_hit(self.ai_keywords)
        exclude_hit = word_hit(self.exclude_keywords)
        return job_hit and ai_hit
    def start_gathering(self):
        self.dict = {}
        last_timestamp = None
        while True:
            url = (
            "https://api.pullpush.io/reddit/search/submission/"
            f"?subreddit={self.subreddit}&after={self.start_ts}"
            f"&before={self.current_before}&size=500"
        )
            r = requests.get(url).json()
            data = r.get("data", [])
            if not data:
                break
            for post in data:
                text = (post.get("title", "") + post.get("text", ""))
                if self.match_keywords(text):
                    pid = post["id"]
                    self.all_ids.append(pid)
                    self.dict[pid] = [post.get("text", ""), post.get("title", "")]
                    if self.amount and len(self.all_ids) >= self.amount:
                        return list(set(self.all_ids)), self.dict
            print("Total matching posts:", len(self.all_ids))
            new_ts = data[-1]["created_utc"]
            if new_ts == last_timestamp:
                print("API stuck at timestamp", new_ts, " — stopping.")
                break

            last_timestamp = new_ts
            self.current_before = new_ts

            if self.current_before <= self.start_ts:
                break

        return list(set(self.all_ids)), self.dict
