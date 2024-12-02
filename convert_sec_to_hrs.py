
def convert_seconds_to_hours(seconds):
    """Wandelt Sekunden in Stunden und Minuten um."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes
