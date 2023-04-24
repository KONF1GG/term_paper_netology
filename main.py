import requests
import json
from private import secret

def download_photos_from_vk(user_id, token_vk):
    response = requests.get(f"https://api.vk.com/method/photos.get?v=5.131&access_token={token_vk}&owner_id={user_id}&album_id=profile&photo_sizes=1&extended=1")
    photos = response.json()['response']['items']
    return photos

if __name__=='__main__':
    print(download_photos_from_vk(secret.id_vk, secret.TOKEN_vk))