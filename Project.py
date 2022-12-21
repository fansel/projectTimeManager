from timetracker import TimeTracker
class Project:
    """Eine Klasse, die Informationen über ein einzelnes Projekt speichert."""
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.time_tracker = TimeTracker()

    def get_total_hours(self):
        """Gibt die Gesamtarbeitszeit für das Projekt zurück."""
        return self.time_tracker.get_total_hours()
