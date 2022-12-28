import datetime
from timerecord import TimeRecord
from project import Project
import timerecord as timerecord
import uuid

class TimeTracker:
    def __init__(self, project):
        """Initialisiert den TimeTracker."""
        self.project = project
        self.start_time = None
        self.end_time = None
        self.duration = 0
        self.description: str = ""
        self.timerecord = TimeRecord(self.start_time, self.end_time)
        self.uuid = uuid.uuid4()
        self.is_running = False

    def start(self):
        """Starts the time tracker and records the current time as the start time."""
        self.start_time = datetime.datetime.now().isoformat()
        self.timerecord= TimeRecord(self.start_time, self.end_time, self.uuid)
        self.is_running = True
        self.save()


    def stop(self):
        """Stops the time tracker and records the current time as the end time."""
        self.end_time = datetime.datetime.now().isoformat()
        self.timerecord.end_time = self.end_time
        self.timerecord.description = self.description
        self.duration = self.timerecord.duration
        

        

    def reset(self):
        """Setzt die Startzeit, Endzeit und Dauer zurück."""
        self.start_time = None
        self.end_time = None
        self.timerecord = TimeRecord(self.start_time, self.end_time)
        self.duration = 0
        self.description = ""
        self.uuid = uuid.uuid4()
        self.is_running = False


    def save(self):
        """Speichert die aktuelle Zeitmessung in der aktuellen Projektdatei."""
        self.project.write_time_record(self.timerecord)


    

