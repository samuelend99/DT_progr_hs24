
# Fiktive Projekte mit 12 Phasen und Stundenbudget für jede Phase
projects = [
    {
        "id": 1,
        "name": "Projekt 1",
        "phases": {
            "Baugesetze klären": {"hours_budget": 10},
            "Vorprojekt Ausarbeiten": {"hours_budget": 5},
            "Baueingabe erstellen": {"hours_budget": 7},
            "Bewilligung": {"hours_budget": 3},
            "Bemusterung": {"hours_budget": 2},
            "Ausführungsplanung": {"hours_budget": 6},
            "Ausschreibung": {"hours_budget": 4},
            "Vergaben und Werkverträge": {"hours_budget": 3},
            "Bauvorbereitung": {"hours_budget": 5},
            "Baukontrolle (Bauleitung)": {"hours_budget": 6},
            "Übergabe": {"hours_budget": 2},
            "2. Jahres Garantie": {"hours_budget": 2}
        }
    },
    {
        "id": 2,
        "name": "Projekt 2",
        "phases": {
            "Baugesetze klären": {"hours_budget": 8},
            "Vorprojekt Ausarbeiten": {"hours_budget": 6},
            "Baueingabe erstellen": {"hours_budget": 6},
            "Bewilligung": {"hours_budget": 4},
            "Bemusterung": {"hours_budget": 3},
            "Ausführungsplanung": {"hours_budget": 5},
            "Ausschreibung": {"hours_budget": 4},
            "Vergaben und Werkverträge": {"hours_budget": 2},
            "Bauvorbereitung": {"hours_budget": 4},
            "Baukontrolle (Bauleitung)": {"hours_budget": 3},
            "Übergabe": {"hours_budget": 3},
            "2. Jahres Garantie": {"hours_budget": 4}
        }
    }
    # Weitere Projekte könnten hier hinzugefügt werden...
]

# Beispielhafte Zeiteinträge für die Phasen
time_entries = [
    {"project_id": 1, "phase": "Baugesetze klären", "hours": 5},
    {"project_id": 1, "phase": "Vorprojekt Ausarbeiten", "hours": 3},
    {"project_id": 1, "phase": "Baueingabe erstellen", "hours": 5},
    {"project_id": 2, "phase": "Baugesetze klären", "hours": 7},
    {"project_id": 2, "phase": "Ausführungsplanung", "hours": 4},
    {"project_id": 2, "phase": "Übergabe", "hours": 2}
    # Weitere Zeiteinträge könnten hier hinzugefügt werden...
]
