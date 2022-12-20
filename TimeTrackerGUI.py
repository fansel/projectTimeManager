import tkinter as tk
from tkinter import ttk, messagebox
from TimeTracker import TimeTracker
from TimeTracker import TimeTracker
import datetime


class TimeTrackerGUI:
    """Eine Klasse, die eine GUI mit einem Play-Pause-Button und einer Tabelle erstellt."""
    def __init__(self, master, tracker):   
        self.tracker = tracker
        self.play_button = tk.Button(master, text="Starten", command=self.on_play_button_click)
        self.play_button.pack()
        self.timetable = ttk.Treeview(master, columns=("date","start", "end", "duration"))
        self.timetable.pack()
        self.clear_button = tk.Button(master, text="Clear", command=self.on_clear_button_click)
        self.clear_button.pack()
        self.hours = tk.Label(master, text="Gesamtstunden: "+str(self.tracker.get_total_hours()))
        self.hours.pack()
        self.export_button = tk.Button(master, text="Exportieren", command=self.on_export_button_click)
        self.export_button.pack()
        self.timetable.heading("#0", text="Datum")
        self.timetable.heading("#1", text="Startzeit")
        self.timetable.heading("#2", text="Endzeit")
        self.timetable.heading("#3", text="Dauer in Minuten")
        self.filter = datetime.datetime.now()
        self.dropdown = tk.OptionMenu(master, self.filter, "Heute", "Letzte Woche", "Letzter Monat", "Letztes Jahr", "Alle")
        self.dropdown.pack()

    def dropdown(self):
        """Wird aufgerufen, wenn ein neuer Filter ausgewählt wird."""
        if self.filter == "Heute":
            self.filter = datetime.date()
        elif self.filter == "Letzte Woche":
            self.filter = datetime.date() - datetime.timedelta(days=7)
        elif self.filter == "Letzter Monat":
            self.filter = datetime.date() - datetime.timedelta(days=30)
        elif self.filter == "Letztes Jahr":
            self.filter = datetime.date() - datetime.timedelta(days=365)
        elif self.filter == "Alle":
            self.filter = 0



    def on_export_button_click(self):
        """Wird aufgerufen, wenn der Export-Button gedrückt wird."""
        messagebox.showinfo("Exportieren", "Exportieren in Arbeit")

    def on_clear_button_click(self):
        """Wird aufgerufen, wenn der Clear-Button gedrückt wird."""
        if self.tracker.start_time is not None:
            tk.messagebox.showerror("Fehler", "Der Tracker läuft bereits.")
            return
        if messagebox.askyesno("Sitzung zurücksetzen?", "Tabelle leeren (Daten werden nicht gelöscht)? "):
            self.timetable.delete(*self.timetable.get_children())
            self.filter = datetime.datetime.now()

    def on_play_button_click(self):
        """Wird aufgerufen, wenn der Play-Button gedrückt wird."""
        if self.tracker.start_time is None:
            # Erfasse die aktuelle Zeit als Startzeit und speichere sie in der JSON-Datei
            self.tracker.start()
            self.tracker.save("times.json")
            self.timetable.insert("", "end", text=self.tracker.start_time["date"], values=(self.tracker.start_time["time"], "", ""))
            self.play_button.config(text="Stoppen")
            self.play_button.config(command=self.on_pause_button_click)
            self.update()



        else:
            # Der Tracker läuft bereits, also zeige eine Fehlermeldung
            tk.messagebox.showerror("Fehler", "Der Tracker läuft bereits.")

    def on_pause_button_click(self):
        """Wird aufgerufen, wenn der Pause-Button gedrückt wird."""
        if self.tracker.start_time is not None:
            # Erfasse die aktuelle Zeit als Endzeit und berechne die Dauer
            self.tracker.stop()
            self.tracker.save("times.json")
            self.tracker.reset()
            self.play_button.config(text="Starten")
            self.play_button.config(command=self.on_play_button_click)
            self.update_table()

        else:
            # Der Tracker läuft nicht, also zeige eine Fehlermeldung
            tk.messagebox.showerror("Fehler", "Der Tracker läuft nicht.")



    def update_table(self):
        self.timetable.delete(*self.timetable.get_children())
        # Lade die Daten aus der JSON-Datei
        data = self.tracker.load("times.json")
        # Setze Standardwerte für Start- und Endzeit sowie Dauer
        start_time = {"date": "", "time": ""}
        end_time = {"date": "", "time": ""}
        duration = ""
        # Überschreibe Standardwerte mit Werten aus der JSON-Datei, wenn vorhanden
        if "start_time" in data:
            start_time = data["start_time"]
        if "end_time" in data:
            end_time = data["end_time"]
        if "duration" in data:
            duration = data["duration"]
        for item in data["time_entries"]:
            if item is not None:
                if item["start_time"]["date"] >= self.filter.strftime("%d.%m.%Y") and item["start_time"]["time"] >= self.filter.strftime("%H:%M:%S"):
                  self.timetable.insert("", "end", text=item["start_time"]["date"], values=(item["start_time"]["time"], item["end_time"]["time"], round(item["duration"], 1)))
        self.hours.config(text="Gesamtstunden: "+str(self.tracker.get_total_hours()))



        
    

def main():
    # Erstelle eine Instanz von TimeTracker
    tracker = TimeTracker()

    # Erstelle ein Fenster
    window = tk.Tk()
    window.title("Time Tracker")

    # Erstelle eine Instanz von TimeTrackerGUI und übergebe das Hauptfenster und den Tracker
    gui = TimeTrackerGUI(window, tracker)
    window.mainloop()
    

if __name__ == "__main__":
    main()    



