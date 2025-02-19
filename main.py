import os
from dotenv import load_dotenv
import requests


def shorten_link(token, url):
    api_url = "https://api.vk.com/method/utils.getShortLink"

    params = {
        "access_token": token,
        "url": url,
        "private": "0",
        "v": "5.199"
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    if "error" in data:
        return "Ошибка: Некорректный URL."

    return data["response"]["short_url"]


def count_clicks(token, shortened_url):
    if "Ошибка" in shortened_url:
        return "Не могу получить статистику: Некорректная сокращенная ссылка."

    key = shortened_url.split("vk.cc/")[1]

    api_url = "https://api.vk.com/method/utils.getLinkStats"

    params = {
        "access_token": token,
        "key": key,
        "interval": "forever",
        "extended": "0",
        "v": "5.199"
    }

    response = requests.get(api_url, params=params)
    clicks = response.json()

    if "response" in clicks and "stats" in clicks["response"]:
        stats = clicks["response"]["stats"]
        if stats:
            return stats[0]["views"]


def is_short_url(url):
    return "vk.cc/" in url


def main():
    url = input("Введите длинную ссылку: ")

    load_dotenv()
    token = os.getenv("VK_TOKEN")

    if is_short_url(url):
        click_count = count_clicks(token, url)
        print("Количество кликов по ссылке:", click_count)
    else:
        shortened_url = shorten_link(token, url)
        print("Сокращенная ссылка:", shortened_url)
        if "Ошибка" not in shortened_url:
            click_count = count_clicks(token, shortened_url)
            print("Количество кликов по ссылке:", click_count)


if __name__ == "__main__":
    main()
