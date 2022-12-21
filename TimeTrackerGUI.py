import tkinter as tk
from tkinter import ttk, messagebox
from timetracker import TimeTracker 
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
        self.hours = tk.Label(master, text="Gesamtstunden: "+str(self.tracker.get_total_hours("times.json")))
        #put the label to the right bottom corner
        self.hours.place(relx=1.0, rely=1.0, anchor='se')
        self.export_button = tk.Button(master, text="Exportieren", command=self.on_export_button_click)
        self.export_button.place(relx=1.0, rely=0.0, anchor='ne')
        self.timetable.heading("#0", text="Datum")
        self.timetable.heading("#1", text="Startzeit")
        self.timetable.heading("#2", text="Endzeit")
        self.timetable.heading("#3", text="Dauer in Minuten")
        self.swichDropdown = tk.StringVar(master)
        self.swichDropdown.set("Seit Programmstart")
        self.progstart = datetime.datetime.now()
        self.filter = self.progstart
        self.update_table()
        self.dropdown = tk.OptionMenu(master, self.swichDropdown, "Seit Programmstart","Heute", "Letzte Woche", "Letzter Monat", "Letztes Jahr", "Alle", command=self.dropdown)  # Add command argument
        #place the dropdown menu to the left of the export button
        self.dropdown.place(relx=0.0, rely=0.0, anchor='nw')
        master.resizable(False, False)
        master.title("TimeTracker")


    def dropdown(self, value):
        """Updates the filter attribute based on the selection in the dropdown menu."""
        if value == "Seit Programmstart":
            self.filter = self.progstart
        elif value == "Heute":
            self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        elif value == "Letzte Woche":
            self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=7)
        elif value == "Letzter Monat":
            self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=30)
        elif value == "Letztes Jahr":
            self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=365)
        elif value == "Alle":
            self.filter = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
        self.update_table()



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
        for item in data["time_entries"]:
            if item["start_time"] is not None:
                start_time = item["start_time"]
            else:
                start_time = {"date": "", "time": ""}
            if item["end_time"] is not None:
                end_time = item["end_time"]
            else:
                end_time = {"date": "", "time": ""}
            if item is not None:
                try: 
                    date_start = datetime.datetime.strptime(item["start_time"]["date"], "%d.%m.%Y").date()
                    time_start = datetime.datetime.strptime(item["start_time"]["time"], "%H:%M:%S").time()
                    start_time = datetime.datetime.combine(date_start, time_start)
                    date_end = datetime.datetime.strptime(item["end_time"]["date"], "%d.%m.%Y").date()
                    time_end = datetime.datetime.strptime(item["end_time"]["time"], "%H:%M:%S").time()
                    end_time = datetime.datetime.combine(date_end, time_end)
                    if start_time >= self.filter:
                        self.timetable.insert("", "end", text=item["start_time"]["date"], values=(item["start_time"]["time"], item["end_time"]["time"],self.tracker.getDurationBetween(start_time, end_time)))
                except:
                    pass
        self.hours.config(text="Gesamtstunden: "+str(self.tracker.get_total_hours("times.json"))+" Stunden")



        
    

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





