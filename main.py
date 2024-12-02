# main.py
from Clockodo_Stunden_aus_Projekte import get_projects, get_time_entries
from convert_sec_to_hrs import convert_seconds_to_hours



if __name__ == "__main__":
    # Projekte abrufen und anzeigen
    print("=== Projekte ===")
    projects = get_projects()
    for project in projects:
        print(f"Projekt-ID: {project['id']}, Name: {project['name']}")

    # Zeitraum und Projekt-ID für Zeiteinträge angeben
    print("\n=== Zeiteinträge ===")
    time_since = "2024-11-01"
    time_until = "2024-11-30"
    project_id = 2719751  # Beispiel-Projekt-ID

    # Zeiteinträge abrufen und anzeigen
    time_entries = get_time_entries(time_since, time_until, project_id)
    for entry in time_entries:
        duration_in_seconds = entry['duration']
        hours, minutes = convert_seconds_to_hours(duration_in_seconds)
        print(f"ID: {entry['id']}, Projekt: {entry['projects_id']}, Dauer: {hours} Stunden {minutes} Minuten, Kommentar: {entry.get('text', 'Kein Kommentar')}")
