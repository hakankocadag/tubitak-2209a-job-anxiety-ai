import requests
import datetime

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
            "job market", "workplace", "workforce"
        ]

        self.ai_keywords = [
            "AI", "Artificial Intelligence", "GPT", "ChatGPT", "Claude", "LLM", "LLMS", "Bing", "LLAMA", "Midjourney", "DALL-E", "generative AI", "Gemini", "Copilot", "Perplexity AI", "Canva", "DeepL", "QuillBot", "Remove.bg", "Grammarly",
            "Character.ai", "Quizizz", "Zapier", "Microsoft Copilot", "CapCut", "DeepAI", "Hugging Face", "Poe", "Suno",
            "ElevenLabs", "InVideo", "Leonardo", "Replit", "Consensus", "Janitor AI", "Runway", "Luma AI", "Filmora", "Otter.ai",
            "DeepSeek", "Stable Diffusion", "Grok", "Microsoft Designer", "you.com", "Synthesia", "Descript", "HeyGen", "Jasper",
            "OpusClip", "Play.ht", "Cursor", "Wordtune", "WriteSonic", "Copy.ai", "Murf.ai", "Pictory", "Pi", "Google AI Studio",
            "Krisp", "Fliki", "Beautiful.ai", "SlidesAI", "NotebookLM", "Groq", "Lumen5", "Rytr", "HyperWrite", "Resemble",
            "Tabnine", "Mem"
        ]

        self.anxiety_keywords = [
            "worried", "anxious", "anxiety", "afraid", "scared",
            "fear", "fearful", "terrified", "panic", "concerned",
            "stress", "stressed", "hopeless", "useless", "future looks bad",
            "overwhelmed", "lose my job", "feels pointless"
        ]

        self.exclude_keywords = [
            "o1", "o3", "benchmark", "latency", "performance", "release",
            "training", "parameters", "architecture", "vision capability",
            "model comparison", "openai update", "claude vs", "gemini vs",
            "project", "tutorial", "my first video", "youtube channel",
            "animation", "subscribe", "check out my", "made this",
            "built this", "tool i made", "explaining how", "how it work",
            "work well", "work properly", "work as a", "work like"
        ]

        self.critical_phrases = [
            "ai replace", "ai replacing", "ai take my job",
            "ai taking my job", "ai taking jobs", "ai will take our jobs",
            "automation replace", "automation replacing",
            "automation taking jobs", "automation taking my job",
            "my job feel unsafe", "threatened by ai",
            "ai job loss", "jobs because of ai"
        ]

    def ts(self, date_str):
        return int(datetime.datetime.strptime(date_str, "%Y-%m-%d").timestamp())

    def match_keywords(self, text):
        t = text.lower()
        job_hit = any(k in t for k in self.job_keywords)
        ai_hit = any(k.lower() in t for k in self.ai_keywords)
        exclude_hit = any(k in t for k in self.exclude_keywords)
        return job_hit and ai_hit and not exclude_hit

    def start_gathering(self):
        self.dict = {}
        while True:
            url = (
                "https://api.pullpush.io/reddit/search/submission/"
                f"?subreddit={self.subreddit}&after={self.start_ts}"
                f"&before={self.current_before}&size=500"
            )
            response = requests.get(url).json()
            data = response.get("data", [])

            if not data:
                break

            for post in data:
                text = (post.get("title", "") + post.get("text", "")).lower()
                if self.match_keywords(text):
                    post_id = post["id"]
                    self.all_ids.append(post_id)
                    self.dict[post_id] = [post.get("text", ""), post.get("title", "")]

            self.current_before = data[-1]["created_utc"]
            print("Total matching posts:", len(self.all_ids))
            if self.current_before <= self.start_ts:
                break

            if len(self.all_ids) >= self.amount:
                break

        return list(set(self.all_ids)), self.dict
