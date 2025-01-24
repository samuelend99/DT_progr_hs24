import pandas as pd
import glob
import re
import os

def load_hours_and_phases_from_file(file_path):
    """
    Lädt die Phasenbezeichner und zugehörigen Stunden aus einer einzelnen Excel-Datei.
    Gibt einen DataFrame mit den Spalten: project_id, phase_name, budget_hours zurück.
    """
    # Projekt-ID aus dem Dateinamen extrahieren, angenommen das Format ist: Budget_Projekt_<ID>.xlsx
    filename = os.path.basename(file_path)
    match = re.search(r"Budget_Projekt_(\d+)\.xlsx", filename)
    if match:
        project_id = int(match.group(1))
    else:
        # Falls kein Muster erkannt wird, kannst du den Nutzerwarnen oder einen Default nehmen
        project_id = None

    try:
        df = pd.read_excel(file_path, sheet_name=1, header=None)
        
        # Zeilen 12 bis 29 (Index 11 bis 28) und Spalten B und G (Index 1 und 6)
        phases = df.iloc[11:32, [1, 6]]  
        phases = phases.dropna()

        # Erstelle einen DataFrame mit eindeutigen Spaltennamen
        phases_df = phases.rename(columns={1: "phase_name", 6: "budget_hours"})
        
        # Füge die project_id-Spalte hinzu
        phases_df["project_id"] = project_id

        return phases_df[["project_id", "phase_name", "budget_hours"]]
    except Exception as e:
        print(f"Fehler beim Laden der Bauphasenstunden aus {file_path}: {e}")
        return pd.DataFrame(columns=["project_id", "phase_name", "budget_hours"])


def load_all_project_budgets(budget_folder="C:\\Users\\se\\Hochbauatelier Dropbox\\Samuel End\\Studium\\3. Semester\\Modul Programming\\Stundenbudget"):
    """
    Durchsucht ein Verzeichnis nach Dateien im Format Budget_Projekt_<ID>.xlsx
    und lädt die Stundenbudgets aller Projekte in einen gemeinsamen DataFrame.
    """
    # Alle Dateien, die mit Budget_Projekt_ und .xlsx enden
    budget_files = glob.glob(os.path.join(budget_folder, "Budget_Projekt_*.xlsx"))
    
    all_dfs = []
    for f in budget_files:
        df = load_hours_and_phases_from_file(f)
        if not df.empty:
            all_dfs.append(df)

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        # Falls keine Dateien gefunden oder alle leer
        return pd.DataFrame(columns=["project_id", "phase_name", "budget_hours"])


# Beispielaufruf:
budget_folder = "C:\\Users\\se\\Hochbauatelier Dropbox\\Samuel End\\Studium\\3. Semester\\Modul Programming\\Stundenbudget"
all_budgets_df = load_all_project_budgets(budget_folder)
print(all_budgets_df)
