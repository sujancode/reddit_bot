class RedditUser:
    def __init__(self,username,password) -> None:
        self.username=username
        self.password=password
        self.client_secret=""
        self.client_id=""