import pandas as pd

def load_hours_and_phases(file_path = "C:\\Users\\se\\Hochbauatelier Dropbox\\Samuel End\\Studium\\3. Semester\\Modul Programming\\Stundenbudget\\Honroarerechnung_test.xlsx"
):
    """
    Lädt die Phasenbezeichner und die zugehörigen Stunden aus dem zweiten Arbeitsblatt eines Excel-Dokuments.
    Erwartet die Daten in Spalte B (Phasenname) und Spalte G (Stunden), Zeilen 12 bis 29.
    """
    try:
        # Lade die Excel-Datei, explizit das zweite Arbeitsblatt auswählen (Index 1, da 0-basiert)
        df = pd.read_excel(file_path, sheet_name=1, header=None)  # Index 1 für das zweite Blatt
        
        # Extrahiere die relevanten Daten: Phasennamen in Spalte B (Index 1) und Stunden in Spalte G (Index 6)
        phases = df.iloc[11:29, [1, 6]]  # Zeilen 12-29 und Spalten B und G
        
        # Entferne NaN-Werte (falls vorhanden)
        phases = phases.dropna()

        # Erstelle ein Dictionary mit Phasen und Stunden
        phase_hours = {}
        for row in phases.itertuples(index=False):
            phase_name = row[0]  # Phasenname aus Spalte B
            hours = row[1]  # Stunden aus Spalte G
            phase_hours[phase_name] = hours
        
        return phase_hours
    except Exception as e:
        print(f"Fehler beim Laden der Bauphasenstunden: {e}")
        return {}

# Beispielaufruf:
file_path ="C:\\Users\\se\\Hochbauatelier Dropbox\\Samuel End\\Studium\\3. Semester\\Modul Programming\\Stundenbudget\\Honroarerechnung_test.xlsx"
hours_per_phase = load_hours_and_phases(file_path)
print(hours_per_phase)
