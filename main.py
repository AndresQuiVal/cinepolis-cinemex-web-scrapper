from bs4 import BeautifulSoup
import requests
import json
import time

def get_soup():
    try:
        response = requests.get("https://cinepolis.com/preventas")
    except requests.exceptions.HTTPError as ex:
        print(f"Error while making request: {ex}")
    else:
        return BeautifulSoup(response.content, 'html.parser')
    

def discord_notify():
    """
    Notifies on discord
    """
    WEBHOOK = 'https://discord.com/api/webhooks/914594039985221742/M71ujxFi8uDjmB6nRh_3o2INHfEv4ChWrz1ORnbTJZpa2S7YAjuWzmUjFdWFq86o1OfJ'
    DEFAULT_IMAGE = 'https://drive.google.com/uc?export=view&id=1LXT2YJDutdnFcEdYhkGh5gmAE-bmoLiG'

    fields = [
        {
            "name": "CINEPOLIS",
            "value": "https://cinepolis.com/preventas",
            "inline": True
        }
    ]

    data = {
        "avatar_url": DEFAULT_IMAGE,
        "username": "Jager Monitor",
        "embeds": [{
            "description": "Accede a Cinepolis para comprar tus boletos de Spiderman: No-Way-Home",
            "color": 16753152,
            "thumbnail": {
                "url": ''
            },
            "fields": fields,
            "footer": {
                "text": f"@jager_bot - 1.0",
                "icon_url": DEFAULT_IMAGE
            }
        }]
    }

    while True:
        r = requests.post(WEBHOOK, data=json.dumps(data), headers={"Content-Type": "application/json"})
        try:
            r.raise_for_status()
            break
        except requests.exceptions.HTTPError as ex:
            print("--- Error al notificar")
            print(ex)
            time.sleep(3)


def main():
    while True:
        print("Inspecting...")
        time.sleep(2)
        soup = get_soup()
        if not soup: 
            continue
        spans = soup.find_all('span', {'class' : 'data-layer'})
        for span in spans:
            title = span['data-titulo'].lower()
            if 'spiderman' in title or 'spider-man' in title or 'spider man' in title:
                discord_notify()
    
if __name__ == "__main__":
    main()