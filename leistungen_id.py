import requests

# Deine API-Informationen
API_TOKEN = "b2657fb7db740ed1e3e2e5d7f105c6d4"  # Ersetze dies durch deinen API-Schlüssel
API_URL = "https://my.clockodo.com/api/services"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",  # Die Authentifizierung im richtigen Format
    "X-Clockodo-External-Application": "MeinPythonScript",  # Optional
}

def get_services():
    try:
        # Anfrage an die Clockodo-API senden
        response = requests.get(API_URL, headers=HEADERS)

        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            services = response.json()
            print("Leistungen (Services) abrufen erfolgreich:")
            for service in services:
                print(f"ID: {service['id']}, Name: {service['name']}")
            return services
        else:
            print(f"Fehler beim Abrufen der Leistungen: {response.status_code}")
            print(response.json())
            return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

# Aufruf der Funktion
if __name__ == "__main__":
    get_services()

