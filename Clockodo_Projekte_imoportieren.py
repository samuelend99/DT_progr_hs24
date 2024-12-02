import requests
from my_secret import API_TOKEN  # Import des Tokens

# API-Konfiguration
API_BASE_URL = "https://my.clockodo.com/api/v2"
API_USER = "se@hochbauatelier.ch"  # E-Mail Clockodo-Accounts
APPLICATION_NAME = "Zeitmanagement"  # Name der Anwendung

def get_projects():
    """
    Ruft die Projekte aus der Clockodo-API ab.
    """
    headers = {
        "X-ClockodoApiUser": API_USER,  # E-Mail-Adresse
        "X-ClockodoApiKey": API_TOKEN,  # API-Token aus my_secret importiert
        "X-Clockodo-External-Application": APPLICATION_NAME,  # Name der externen Anwendung
        "Content-Type": "application/json"  # JSON-Format
    }
    
    try:
        # Endpunkt für Projekte
        response = requests.get(f"{API_BASE_URL}/projects", headers=headers)
        if response.status_code == 200:
            print("Projekte erfolgreich abgerufen.")
            return response.json()["projects"]
        else:
            print(f"Fehler beim Abrufen der Projekte: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist bei der API-Anfrage aufgetreten: {e}")
        return []

# Testaufruf
if __name__ == "__main__":
    projects = get_projects()
    for project in projects:
        print(f"Projekt-ID: {project['id']}, Name: {project['name']}")
