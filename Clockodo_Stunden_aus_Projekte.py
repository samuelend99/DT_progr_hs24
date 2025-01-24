# clockodo_api.py
import requests
from config import API_BASE_URL, API_USER, APPLICATION_NAME, API_TOKEN

def get_projects():
    """
    Ruft die Projekte aus der Clockodo-API ab.
    """
    headers = {
        "X-ClockodoApiUser": API_USER,
        "X-ClockodoApiKey": API_TOKEN,
        "X-Clockodo-External-Application": APPLICATION_NAME,
        "Content-Type": "application/json"
    }

    try:
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

def get_time_entries(time_since, time_until, project_id=None):
    headers = {
        "X-ClockodoApiUser": API_USER,
        "X-ClockodoApiKey": API_TOKEN,
        "X-Clockodo-External-Application": APPLICATION_NAME,
        "Content-Type": "application/json",
    }

    params = {
        "time_since": f"{time_since}T00:00:00Z",
        "time_until": f"{time_until}T23:59:59Z",
    }

    if project_id:
        params["filter[projects_id]"] = project_id

    try:
        response = requests.get(f"{API_BASE_URL}/entries", headers=headers, params=params)
        print("API-Request URL:", response.url)  # Debugging
        if response.status_code == 200:
            print("Zeiteinträge erfolgreich abgerufen.")
            return response.json().get("entries", [])
        else:
            print(f"Fehler beim Abrufen der Zeiteinträge: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist bei der API-Anfrage aufgetreten: {e}")
        return []


def get_services():
    """
    Ruft die Leistungen aus der Clockodo-API ab.
    """
    headers = {
        "X-ClockodoApiUser": API_USER,
        "X-ClockodoApiKey": API_TOKEN,
        "X-Clockodo-External-Application": APPLICATION_NAME,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{API_BASE_URL}/services", headers=headers)
        if response.status_code == 200:
            print("Leistungen erfolgreich abgerufen.")
            return response.json()["services"]
        else:
            print(f"Fehler beim Abrufen der Leistungen: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist bei der API-Anfrage aufgetreten: {e}")
        return []

def convert_seconds_to_hours(seconds):
    """Wandelt Sekunden in Stunden und Minuten um."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes
