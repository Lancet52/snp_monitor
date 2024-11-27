import requests
import json
from rich.console import Console

console = Console()


def start():
    console.print("""
███████ ███    ██ ██████      ███    ███  ██████  ███    ██ ██ ████████  ██████  ██████  
██      ████   ██ ██   ██     ████  ████ ██    ██ ████   ██ ██    ██    ██    ██ ██   ██ 
███████ ██ ██  ██ ██████      ██ ████ ██ ██    ██ ██ ██  ██ ██    ██    ██    ██ ██████  
     ██ ██  ██ ██ ██          ██  ██  ██ ██    ██ ██  ██ ██ ██    ██    ██    ██ ██   ██ 
███████ ██   ████ ██          ██      ██  ██████  ██   ████ ██    ██     ██████  ██   ██ 
                                                                      
""", style="blue")
    console.print("Введите никнейм: ", style="yellow")
    search_username()


def search_username():
    username = input()

    with open("websites.json", "r") as f:
        file_json = json.load(f)
    listdir = []
    for data in file_json["items"]:
        url_old = data["url"]
        url_new = url_old.replace("{}", f"{username}")
        response = requests.get(f'{url_new}')

        if response.status_code == 200:
            console.print(f"{data["domain"]}  {data["name"]}  {url_new}", style="green")
            listdir.append(f"{data["name"]}  {url_new}")
        else:
            console.print(f"{data["domain"]}  {data["name"]}: Нет данных", style="red")
    f.close()

    console.print("========================================\nПоиск закончен ", style="yellow")

    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(f"Ресурсы на которых есть пользователь с ником {username}\n\n")
        for index in listdir:

            file.write(f"{index}\n")
    file.close()

    return


if __name__ == '__main__':
    start()
