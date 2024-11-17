import requests

# API-Konfiguration
API_BASE_URL = "https://my.clockodo.com/api/v2"
API_TOKEN = "xyz"  # Clockodo API-Schlüssel
API_USER = "se@hochbauatelier.ch"  # E-Mail deines Clockodo-Accounts
APPLICATION_NAME = "Zeitmanagment"  # Name der Anwendung

def get_projects():
    """
    Ruft die Projekte aus der Clockodo-API ab.
    """
    headers = {
        "X-ClockodoApiUser": API_USER,  # E-Mail-Adresse
        "X-ClockodoApiKey": API_TOKEN,  # API-Token
        "X-Clockodo-External-Application": APPLICATION_NAME,  # Name der externen Anwendung
        "Content-Type": "application/json"  # JSON-Format
    }
    
    try:
        response = requests.get(f"{API_BASE_URL}/customers", headers=headers)
        if response.status_code == 200:
            print("Projekte erfolgreich abgerufen.")
            return response.json()["customers"]
        else:
            print(f"Fehler beim Abrufen der Projekte: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return []

if __name__ == "__main__":
    projects = get_projects()
    if projects:
        for project in projects:
            print(f"Projektname: {project['name']}, ID: {project['id']}")
    else:
        print("Keine Projekte gefunden.")
