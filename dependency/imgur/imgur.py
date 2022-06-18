
class ImgurWrapper:
    
    def __init__(self,client_id,requests,extension_util) -> None:
        self.client_id=client_id
        self.requests=requests
        self.get_extension_from_url=extension_util


    def upload_to_imgur(self,url):
        upload_url = "https://api.imgur.com/3/image"
        headers = {
        'Authorization': f'Client-ID {self.client_id}'
        }

        file_info=self.get_extension_from_url(url)

        if file_info:
            [filename,extension]=file_info
            res=self.requests.get(url)

            with self.requests.Session() as session:
                data={
                    "image":res.content,
                    "filename":filename
                }
                response = session.post(upload_url, headers=headers, data=data)
                if response.status_code ==200:
                    return response.text
        return None
    