import pandas as pd
from Clockodo_Stunden_aus_Projekte import get_time_entries, get_projects, get_services, convert_seconds_to_hours
from stundenbudget_excel import load_all_project_budgets  # Passe den Import entsprechend dem Skriptnamen an

# Beispiel: Zeitrahmen und Projekt-ID aus Clockodo wählen
time_since = "2024-11-01"
time_until = "2024-11-30"

# Projekte abrufen, um Projekt-ID zu bekommen (falls noch nicht bekannt)
projects = get_projects()

# Angenommen, wir wollen ein bestimmtes Projekt verarbeiten
# Zum Beispiel das erste Projekt aus der Liste oder ein spezifisches Projekt nach Name:
selected_project = projects[0]  # oder ein Filter nach Name
project_id = selected_project['id']

# 1. Zeiteinträge für das Projekt abrufen
entries = get_time_entries(time_since, time_until, project_id=project_id)
entries_df = pd.DataFrame(entries)

if entries_df.empty:
    print("Keine Zeiteinträge für dieses Projekt in diesem Zeitraum gefunden.")
else:
    # Dauer in Stunden umrechnen
    entries_df["used_hours"] = entries_df["duration"] / 3600.0

    # 2. Leistungen abrufen und mapping erstellen
    services = get_services()
    services_df = pd.DataFrame(services)
    # services_df sollte Spalten wie "id" und "name" haben
    # Erstelle ein Dict zum Mappen von services_id auf service_name
    service_mapping = dict(zip(services_df["id"], services_df["name"]))

    # Mappe services_id -> service_name
    entries_df["service_name"] = entries_df["services_id"].map(service_mapping)

    # Nun gruppieren wir nach project_id und service_name, um die Gesamtstunden pro Leistung zu summieren
    used_hours_df = entries_df.groupby(["project_id", "service_name"], as_index=False)["used_hours"].sum()

    # 3. Budget-Daten laden
    all_budgets_df = load_all_project_budgets()  # Liefert project_id, phase_name, budget_hours
    # Filter für das ausgewählte Projekt
    project_budget_df = all_budgets_df[all_budgets_df["project_id"] == project_id]

    if project_budget_df.empty:
        print("Keine Budgetdaten für dieses Projekt gefunden.")
    else:
        # 4. Merge durchführen
        # Wir nehmen an, dass 'phase_name' in den Budgetdaten dem 'service_name' in Clockodo entspricht.
        # Falls nicht, musst du hier ein Mapping einbauen.
        merged_df = pd.merge(project_budget_df, used_hours_df, left_on=["project_id", "phase_name"],
                             right_on=["project_id", "service_name"], how="left")

        # Falls es Leistungen im Budget gibt, für die es noch keine Zeiteinträge gibt, steht used_hours NaN
        # Ersetze NaN durch 0
        merged_df["used_hours"] = merged_df["used_hours"].fillna(0)

        # Verbleibende Stunden berechnen
        merged_df["remaining_hours"] = merged_df["budget_hours"] - merged_df["used_hours"]

        # 5. Ausgabe
        print("Stundenübersicht für Projekt:", project_id)
        print(merged_df[["phase_name", "budget_hours", "used_hours", "remaining_hours"]])

        # Gesamtsummen fürs Projekt
        total_budget = merged_df["budget_hours"].sum()
        total_used = merged_df["used_hours"].sum()
        total_remaining = merged_df["remaining_hours"].sum()

        print("\nGesamtsummen für das Projekt:")
        print(f"Budget insgesamt: {total_budget:.2f} h")
        print(f"Verbraucht: {total_used:.2f} h")
        print(f"Verbleibend: {total_remaining:.2f} h")
