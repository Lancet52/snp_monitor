import requests
import json

import urllib3.exceptions
from rich.console import Console
from bs4 import BeautifulSoup

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
            try:
                response = requests.get(url=url_new, headers={'User-Agent': 'Mozilla/5.0'}, timeout=7)
                if response.status_code == 404:
                    console.print(f"{data["domain"]}  {data["name"]}: Нет данных", style="red")
                elif response.status_code == 200:
                    console.print(f"{data["domain"]}  {data["name"]}  {url_new}", style="green")
                    listdir.append(f"{data["name"]}  {url_new}")
                else:
                    console.print(f"{data["domain"]}  {data["name"]}: Нет данных", style="red")
            except requests.Timeout:
                console.print(f"{data["domain"]}  {data["name"]}: Истёк таймаут подключения", style="yellow")
            except requests.RequestException:
                console.print(f"{data["domain"]}  {data["name"]}: Ошибка при доступе. Истёк таймаут подулючения",
                              style="yellow")

        elif data["errorType"] == "message":
            try:
                response = requests.get(url=url_new, headers={'User-Agent': 'Mozilla/5.0'}, timeout=7)
                soup = BeautifulSoup(response.text, "html.parser")
                error_text = data["errorMsg"]
                res_soup = soup.find(string=f"{error_text}")
                if response.status_code == 404:
                    console.print(f"{data["domain"]}  {data["name"]}: Нет данных", style="red")

                elif response.status_code == 200:

                    if res_soup is not None:
                        console.print(f"{data["domain"]}  {data["name"]}: Нет данных", style="red")
                    else:
                        console.print(f"{data["domain"]}  {data["name"]}  {url_new}", style="green")
                        listdir.append(f"{data["name"]}  {url_new}")
                else:
                    console.print(f"{data["domain"]}  {data["name"]}: Нет данных", style="red")
            except requests.Timeout:
                console.print(f"{data["domain"]}  {data["name"]}: Истёк таймаут подключения", style="yellow")
            except requests.RequestException:
                console.print(f"{data["domain"]}  {data["name"]}: Ошибка при доступе. Истёк таймаут подключения",
                              style="yellow")

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
