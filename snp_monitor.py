import requests
import json

import urllib3.exceptions
from rich.console import Console
from bs4 import BeautifulSoup

from snp_basefunctions import status_code, message

console = Console()


def start():
    console.print("""
███████ ███    ██ ██████      ███    ███  ██████  ███    ██ ██ ████████  ██████  ██████  
██      ████   ██ ██   ██     ████  ████ ██    ██ ████   ██ ██    ██    ██    ██ ██   ██ 
███████ ██ ██  ██ ██████      ██ ████ ██ ██    ██ ██ ██  ██ ██    ██    ██    ██ ██████  
     ██ ██  ██ ██ ██          ██  ██  ██ ██    ██ ██  ██ ██ ██    ██    ██    ██ ██   ██ 
███████ ██   ████ ██          ██      ██  ██████  ██   ████ ██    ██     ██████  ██   ██ 
                                                                      
""", style="blue")
    console.print("""Выберите действие:\n\n[1] - Поиск по никнейму""")
    if input() == "1":
        search_username()
    else:
        start()
    return


def search_username():
    console.print("Введите никнейм: ", style="yellow")
    username = input()

    with open("websites.json", "r") as websites_file:
        file_json = json.load(websites_file)
    listdir = []
    for data in file_json["items"]:
        url_old = data["url"]
        url_new = url_old.replace("{}", f"{username}")

        # Если тип ошибки Status Code (нет отклика от страницы)
        if data["errorType"] == "status_code":
            status_code(listdir, data, url_new)

        elif data["errorType"] == "message":
            message(listdir, data, url_new)

        websites_file.close()

    console.print("========================================\nПоиск закончен\n", style="yellow")
    console.print(
        "===========================================================================\nРезультат сохранен в  файл [blue underline]result.txt[/blue underline] кореневой папке с программой",
        style="yellow")

    with open("result.txt", "w", encoding="utf-8") as result_file:
        result_file.write(f"Ресурсы на которых есть пользователь с ником {username}\n\n")
        for index in listdir:
            result_file.write(f"{index}\n")
    result_file.close()

    return


if __name__ == '__main__':
    start()
