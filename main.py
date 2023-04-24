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

def save_photo_to_yandex_disk(photo, token):
    photo_sizes = photo["sizes"]
    max_size = max(photo_sizes, key=lambda x: x['height'] * x['width'])
    url = max_size["url"]
    likes = photo["likes"]["count"]
    file_name = f"{likes}.jpg"
    response = save_to_yandex_disk(token, url, file_name)

    if response.get("error"):
        if response["error"].get["massage"] == "409 Conflict":
            date = photo["date"]
            file_name += f'_{date}'
            response = save_to_yandex_disk(token, url, file_name)

        print(f"Ошибка сохранения на Я.Диск: {response['error']}")
    else:
        print(f"Фото {file_name} сохранено на Я.Диске")

    return {"file_name": file_name, "size": max_size["type"], "likes": likes}

if __name__=='__main__':
    pprint(download_photos_from_vk(secret.id_vk, secret.TOKEN_vk))