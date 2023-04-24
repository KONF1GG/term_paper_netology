import requests
import json
from private import secret
from pprint import pprint

def download_photos_from_vk(user_id, token_vk):
    response = requests.get(f"https://api.vk.com/method/photos.get?v=5.131&access_token={token_vk}&owner_id={user_id}&album_id=profile&photo_sizes=1&extended=1")
    photos = response.json()['response']['items']
    return photos

def save_to_yandex_disk(token, url, file_name):
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": f"/{file_name}", "url": url}
    response = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload", headers=headers, params=params)
    return response.json()

if __name__=='__main__':
    pprint(download_photos_from_vk(secret.id_vk, secret.TOKEN_vk))