
# Funktion zur Berechnung der verbleibenden Stunden pro Projekt und Phase
def calculate_remaining_hours(projects, time_entries):
    # Für jedes Projekt die verbleibenden Stunden berechnen
    for project in projects:
        print(f"Projekt: {project['name']}")
        for phase, data in project['phases'].items():
            # Stundenbudget für die Phase holen
            budget = data["hours_budget"]
            # Stunden aus den Zeiteinträgen summieren
            hours_spent = sum(entry['hours'] for entry in time_entries if entry['project_id'] == project['id'] and entry['phase'] == phase)
            # Verbleibende Stunden berechnen
            remaining_hours = budget - hours_spent
            print(f"  {phase}: {remaining_hours} Stunden verbleibend (Budget: {budget}, Aufgewendete Stunden: {hours_spent})")
        print("-" * 50)
