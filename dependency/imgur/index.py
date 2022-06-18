
from dependency.imgur.imgur import ImgurWrapper
import requests

ImgUr_WRAPPER_INSTANCE=None


def get_extension_from_url(url):
    url_comp=url.split("/")
    filename=url_comp[-1]
    if "." in filename:
        return filename.split(".")
    return None


def getImgurWrapperInstance():
    global ImgUr_WRAPPER_INSTANCE

    if not ImgUr_WRAPPER_INSTANCE:
        ImgUr_WRAPPER_INSTANCE = ImgurWrapper(client_id="9f3f5f6d63f736f",requests=requests,extension_util=get_extension_from_url)
    return ImgUr_WRAPPER_INSTANCE