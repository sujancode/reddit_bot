class RedditWrapper:
    def __init__(self,reddit,json,db) -> None:
        self.reddit=reddit
        self.json=json
        self.db=db

    def get_account_banned_status(self):
        return self.reddit.user.me().subreddit.user_is_banned
    
    def get_random_name(self,browser):
        random_name_url="https://old.reddit.com/api/v1/generate_username.json"
        browser.get(random_name_url)
        body=browser.find_element_by_css_selector("body").text
        body=self.json.loads(body)
        return body["usernames"][0]

    def scrape_top_posts_from_subreddit(self,subreddit):
        subreddit=self.reddit.subreddit(subreddit).hot(limit=25)
        return [item for item in subreddit]
            

    def get_subreddits_by_type(self,type):
        collection="subreddits"
        collections=self.db.find_one(collection,{'type':type})
        return [item for item in collections["subreddits"]]
    
    def get_posts(self):
        collection="posts"
        return self.db.find_all(collection)
    
    def post_with_title_url(self,subreddit,title,url):
        subreddit=self.reddit.subreddit(subreddit)
        subreddit.submit(title=title,url=url)
    
    def pin_to_post(self,subreddit,title,url):
        subreddit=self.reddit.subreddit(f"u_{subreddit}")
        submisson=subreddit.submit(title=title,url=url)
        submisson.mod.sticky()