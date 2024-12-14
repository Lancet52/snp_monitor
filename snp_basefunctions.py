import requests
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()


def status_code(listdir, data, url_new):
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


def message(listdir, data, url_new):
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
