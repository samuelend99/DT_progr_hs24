# main.py
import pandas as pd
from Clockodo_Stunden_aus_Projekte import get_projects, get_time_entries, get_services, convert_seconds_to_hours
from stundenbudget_excel import load_all_project_budgets  # Stelle sicher, dass dieses Skript richtig importiert wird

if __name__ == "__main__":
    # Zeitraum für Zeiteinträge
    time_since = "2024-11-01"
    time_until = "2024-11-30"
    
    # Beispiel-Projekt-ID (aus Clockodo)
    project_id = 3052474

    # Zeiteinträge abrufen
    entries = get_time_entries(time_since, time_until, project_id)
    entries_df = pd.DataFrame(entries)

    if entries_df.empty:
        print("Keine Zeiteinträge für dieses Projekt in diesem Zeitraum gefunden.")
        exit()

    # Falls 'projects_id' statt 'project_id' vorhanden ist, umbenennen
    if 'projects_id' in entries_df.columns:
        entries_df.rename(columns={'projects_id': 'project_id'}, inplace=True)

    # Dauer in Stunden umrechnen
    entries_df["used_hours"] = entries_df["duration"] / 3600.0

    # Leistungen abrufen und Mapping erstellen
    services = get_services()
    services_df = pd.DataFrame(services)
    service_mapping = dict(zip(services_df["id"], services_df["name"]))

    # service_name hinzufügen
    entries_df["service_name"] = entries_df["services_id"].map(service_mapping)

    # Verbrauchte Stunden pro Leistung aggregieren
    if "project_id" not in entries_df.columns or "service_name" not in entries_df.columns:
        print("Benötigte Spalten 'project_id' oder 'service_name' fehlen.")
        exit()

    used_hours_df = entries_df.groupby(["project_id", "service_name"], as_index=False)["used_hours"].sum()

    # Budget-Daten laden und für das ausgewählte Projekt filtern
    all_budgets_df = load_all_project_budgets()
    project_budget_df = all_budgets_df[all_budgets_df["project_id"] == project_id]

    if project_budget_df.empty:
        print("Keine Budgetdaten für dieses Projekt gefunden.")
        exit()

    # Merge von Budget und verwendeten Stunden
    # Annahme: phase_name == service_name
    merged_df = pd.merge(project_budget_df, used_hours_df, left_on=["project_id", "phase_name"],
                         right_on=["project_id", "service_name"], how="left")

    # fehlende (noch nicht verwendete) Leistungen mit 0 auffüllen
    merged_df["used_hours"] = merged_df["used_hours"].fillna(0)

    # Verbleibende Stunden berechnen
    merged_df["remaining_hours"] = merged_df["budget_hours"] - merged_df["used_hours"]

    # Ergebnisse anzeigen
    print("Stundenübersicht pro Leistung:")
    for _, row in merged_df.iterrows():
        print(f"Leistung: {row['phase_name']}, Budget: {row['budget_hours']}h, Verbraucht: {row['used_hours']}h, Verbleibend: {row['remaining_hours']}h")

    # Gesamtsummen
    total_budget = merged_df["budget_hours"].sum()
    total_used = merged_df["used_hours"].sum()
    total_remaining = merged_df["remaining_hours"].sum()

    print("\nGesamtübersicht:")
    print(f"Budget insgesamt: {total_budget:.2f}h")
    print(f"Verbraucht: {total_used:.2f}h")
    print(f"Verbleibend: {total_remaining:.2f}h")

