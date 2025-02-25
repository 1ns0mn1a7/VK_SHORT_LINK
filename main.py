import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


class VKAPIError(Exception):
    pass


def shorten_link(token, url):
    api_url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "access_token": token,
        "url": url,
        "private": "0",
        "v": "5.199"
    }
    response = requests.get(api_url, params=params).json()
    if "error" in response:
        raise VKAPIError(f"Ошибка: {response['error']['error_msg']}")
    return response["response"]["short_url"]


def count_clicks(token, shortened_url):
    key = urlparse(shortened_url).path.lstrip('/')
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "key": key,
        "interval": "forever",
        "extended": "0",
        "v": "5.199"
    }
    response = requests.get(api_url, params=params).json()
    if "error" in response:
        raise VKAPIError(f"Ошибка: {response['error']['error_msg']}")
    stats = response.get("response", {}).get("stats", [{}])
    return stats[0].get("views", None)


def is_shorten_link(token, url):
    key = urlparse(url).path.lstrip('/')
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "key": key,
        "interval": "forever",
        "extended": "0",
        "v": "5.199"
    }
    response = requests.get(api_url, params=params).json()
    return "error" not in response


def main():
    load_dotenv()
    token = os.environ["VK_TOKEN"]

    url = input("Введите ссылку: ")

    try:
        if is_shorten_link(token, url):
            clicks = count_clicks(token, url)
            print(
                "Количество кликов по ссылке:",
                clicks or "Статистики пока нет."
            )
        else:
            shortened_url = shorten_link(token, url)
            print(
                "Сокращённая ссылка:",
                shortened_url
            )

    except VKAPIError as error:
        print(error)


if __name__ == "__main__":
    main()
