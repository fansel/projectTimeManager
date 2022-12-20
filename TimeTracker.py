
import datetime
import json

class TimeTracker:
    """Eine Klasse, die die Arbeitszeiten verwaltet und in einer JSON-Datei speichert."""
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.timestamp = None
    
    def start(self):
        """Erfasst die aktuelle Zeit als Startzeit."""
        self.start_time = self.get_current_time()
        self.timestamp = datetime.datetime.now()

    def stop(self):
        """Erfasst die aktuelle Zeit als Endzeit und berechnet die Dauer in Minuten."""
        self.end_time = self.get_current_time()
        start = datetime.datetime.strptime(self.start_time["time"], "%H:%M:%S")
        end = datetime.datetime.strptime(self.end_time["time"], "%H:%M:%S")
        duration = end - start
        self.duration = duration.total_seconds() / 60
        

    def reset(self):
        """Setzt die Startzeit, Endzeit und Dauer zurück."""
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.timestamp = None

    def save(self, filename,):
        """Speichert die Startzeit, Endzeit und Dauer in der JSON-Datei."""
        found = False
        try:
            with open(filename, "r") as read_file:
                data = json.load(read_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {"time_entries": []}
        for entry in data["time_entries"]:
            if entry["start_time"] == self.start_time:
                entry["end_time"] = self.end_time
                entry["duration"] = self.duration
                found = True
                break
        if not found:
            data["time_entries"].append({
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.duration
            })
          
        with open(filename, "w") as write_file:
            json.dump(data, write_file, indent=4)


    def load(self, filename):
        """Lädt die Startzeit, Endzeit und Dauer aus der JSON-Datei."""
        with open(filename, "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def get_current_time():
        """Erfasst die aktuelle Zeit und das aktuelle Datum und gibt sie als Dictionary zurück."""
        current_time = datetime.datetime.now()
        return {
            "date": current_time.strftime("%d.%m.%Y"),
            "time": current_time.strftime("%H:%M:%S")
        }

    def get_total_hours(self):
        """Gibt die Summe der Dauer aller Einträge in der JSON-Datei zurück."""
        total_hours = 0
        with open("times.json", "r") as f:
            data = json.load(f)
        for entry in data["time_entries"]:
            if entry["duration"] is not None:
                total_hours += entry["duration"]
        total_hours = round(total_hours /60, 2)
        return total_hours 

