import json
import datetime

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.duration = None

        

    def start(self):
        """Starts the time tracker and records the current time as the start time."""
        self.start_time = {"date": datetime.date.today().strftime("%d.%m.%Y"), "time": datetime.datetime.now().strftime("%H:%M:%S")}

    def stop(self):
        """Stops the time tracker and records the current time as the end time."""
        self.end_time = {"date": datetime.date.today().strftime("%d.%m.%Y"), "time": datetime.datetime.now().strftime("%H:%M:%S")}
        self.duration = self.get_duration()

    def get_duration(self):
        """Calculates the duration of the time tracker in minutes."""

        date_start = datetime.datetime.strptime(self.start_time["date"], "%d.%m.%Y").date()
        time_start = datetime.datetime.strptime(self.start_time["time"], "%H:%M:%S").time()
        start_time = datetime.datetime.combine(date_start, time_start)
        date_end = datetime.datetime.strptime(self.end_time["date"], "%d.%m.%Y").date()
        time_end = datetime.datetime.strptime(self.end_time["time"], "%H:%M:%S").time()
        end_time = datetime.datetime.combine(date_end, time_end)
        duration = (end_time - start_time).total_seconds() / 60
        rounded_duration = round(duration)
        return rounded_duration





    def reset(self):
        """Setzt die Startzeit, Endzeit und Dauer zurück."""
        self.start_time = None
        self.end_time = None
    def save(self, filename):
        try:
            with open(filename, "r") as read_file:
                data = json.load(read_file)
        except json.decoder.JSONDecodeError:
            data = {"time_entries": []}
        except FileNotFoundError:
            with open(filename, 'x') as f:
                pass
            data = {"time_entries": []}
        found = False
        for entry in data["time_entries"]:
            if entry["start_time"] == self.start_time:
                entry["end_time"] = self.end_time
                found = True
                break
        if not found:
            data["time_entries"].append({
                "start_time": self.start_time,
                "end_time": self.end_time,
            })
        with open(filename, "w") as write_file:
            json.dump(data, write_file, indent=4)


                
            
            

    def load(self, filename):
        """Loads the start and end times of the time tracker from a JSON file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                return data
        except json.decoder.JSONDecodeError or FileNotFoundError:
            return {"time_entries": []}

    def get_total_hours(self, filename):
        """Gibt die Gesamtarbeitszeit für das Projekt zurück."""
        try:
            with open(filename, "r") as read_file:
                data = json.load(read_file)
                total = 0
                for entry in data["time_entries"]:
                    if entry["start_time"] == None:
                        continue
                    elif entry["start_time"] == "Null":
                        continue
                    elif entry["end_time"] == "Null":
                        continue
                    elif entry["end_time"] == None:
                        continue

                    date_start = datetime.datetime.strptime(entry["start_time"]["date"], "%d.%m.%Y").date()
                    time_start = datetime.datetime.strptime(entry["start_time"]["time"], "%H:%M:%S").time()
                    start_time = datetime.datetime.combine(date_start, time_start)
                    date_end = datetime.datetime.strptime(entry["end_time"]["date"], "%d.%m.%Y").date()
                    time_end = datetime.datetime.strptime(entry["end_time"]["time"], "%H:%M:%S").time()
                    end_time = datetime.datetime.combine(date_end, time_end)
                    duration = (end_time - start_time).total_seconds() / 3600
                    total += duration
                return round(total,2)
        except json.decoder.JSONDecodeError:
            return 0
        except FileNotFoundError: 
            with open(filename, 'x') as f:
                pass
        


    def getDurationBetween(self, start, end):
        duration = (end - start).total_seconds() / 60
        return round(duration,1)


