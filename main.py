import requests
import json
from private import secret

def download_photos_from_vk(user_id, token_vk):
    response = requests.get(f"https://api.vk.com/method/photos.get?v=5.131&access_token={token_vk}&owner_id={user_id}&album_id=profile&photo_sizes=1&extended=1")
    photos = response.json()['response']['items']
    return photos

def create_folder_on_yandex_disk(token, folder_name):
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": folder_name}
    response = requests.put("https://cloud-api.yandex.net/v1/disk/resources", headers=headers, params=params)
    return response.json()

def save_to_yandex_disk(token, url, folder_name, file_name):
    headers = {"Authorization": f"OAuth {token}"}

    # проверим, есть ли папка на Яндекс.Диске
    params = {"path": f"/{folder_name}/{file_name}"}
    response = requests.put("https://cloud-api.yandex.net/v1/disk/resources/upload", headers=headers, params=params)
    if response.status_code == 409:  # папка уже есть на Я.Диске
        params = {"path": f"/{folder_name}/{file_name}", "url": url}
    else:
        create_folder_on_yandex_disk(yandex_token, folder_name)
        params = {"path": f"/{folder_name}/{file_name}", "url": url}
    response = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload", headers=headers, params=params)
    return response.json()

def save_vk_photos_to_yandex_disk(user_id, vk_token, yandex_token):
    photos = download_photos_from_vk(user_id, vk_token)
    results = []
    unique_likes = []
    folder_name = f"vk_photos_{user_id}"

    for photo in photos:
        photo_sizes = photo["sizes"]
        max_size = max(photo_sizes, key=lambda x: x['height'] * x['width'])
        url = max_size["url"]
        likes = photo["likes"]["count"]
        if likes in unique_likes:
            file_name = f"{likes}_{photo['date']}.jpg"
        else:
            unique_likes.append(likes)
            file_name = f"{likes}.jpg"
        response = save_to_yandex_disk(yandex_token, url, folder_name, file_name)

        if response.get("error"):
            print(f"Ошибка сохранения на Я.Диск: {response['error']}")
        else:
            print(f"Фото {file_name} сохранено на Я.Диске")

        results.append({"file_name": file_name, "size": max_size["type"], "likes": likes})

        with open("vk_photos_info.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    print("Информация о фотографиях сохранена в файле vk_photos_info.json")

if __name__ == '__main__':
    # user_id = input("Введите id пользователя VK: ")
    # vk_token = input("Введите токен VK API: ")
    # yandex_token = input("Введите токен Яндекс.Диска: ")
    user_id = secret.id_vk
    vk_token = secret.TOKEN_vk
    yandex_token = secret.TOKEN_YA

    save_vk_photos_to_yandex_disk(user_id, vk_token, yandex_token)