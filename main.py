# main.py
from test_data import projects, time_entries
from calculate_time import calculate_remaining_hours

# Aufruf der Berechnungsfunktion, um die verbleibenden Stunden zu berechnen
calculate_remaining_hours(projects, time_entries)
