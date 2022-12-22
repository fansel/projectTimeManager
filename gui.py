from doctest import master
from hashlib import new
from re import S
import tkinter as tk
from tkinter import ttk, messagebox
from timetracker import TimeTracker 
import datetime
from application import Application

class Gui:
    """Eine Klasse, die eine GUI mit einem Play-Pause-Button und einer Tabelle erstellt."""
    def __init__(self, master, app):   
        self.app = app
        self.tracker = app.current_tracker
        self.project = app.current_project
        self.play_button = tk.Button(master, text="Starten", command=self.on_play_button_click)
        self.play_button.pack()
        self.timetable = ttk.Treeview(master, columns=("date","start", "end", "duration"))
        self.timetable.pack()
        self.clear_button = tk.Button(master, text="Clear", command=self.on_clear_button_click)
        self.clear_button.pack()
        self.hours = tk.Label(master, text="Gesamtstunden: "+str(self.project.get_total_hours()))
        #put the label to the right bottom corner
        self.hours.place(relx=1.0, rely=1.0, anchor='se')
        # self.export_button = tk.Button(master, text="Exportieren", command=self.on_export_button_click)
        # self.export_button.place(relx=1.0, rely=0.0, anchor='ne')
        self.timetable.heading("#0", text="Datum")
        self.timetable.heading("#1", text="Startzeit")
        self.timetable.heading("#2", text="Endzeit")
        self.timetable.heading("#3", text="Dauer in Minuten")
        # self.swichDropdown = tk.StringVar(master)
        # self.swichDropdown.set("Seit Programmstart")
        # self.progstart = datetime.datetime.now()
        # self.filter = self.progstart
        self.loadTableOnStart()
        # self.dropdown = tk.OptionMenu(master, self.swichDropdown, "Seit Programmstart","Heute", "Letzte Woche", "Letzter Monat", "Letztes Jahr", "Alle", command=self.dropdown)  # Add command argument
        #place the dropdown menu to the left of the export button
        # self.dropdown.place(relx=0.0, rely=0.0, anchor='nw')
        master.resizable(False, False)
        master.title(self.project.name)


    # def dropdown(self, value):
    #     """Updates the filter attribute based on the selection in the dropdown menu."""
    #     if value == "Seit Programmstart":
    #         self.filter = self.progstart
    #     elif value == "Heute":
    #         self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    #     elif value == "Letzte Woche":
    #         self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=7)
    #     elif value == "Letzter Monat":
    #         self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=30)
    #     elif value == "Letztes Jahr":
    #         self.filter = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=365)
    #     elif value == "Alle":
    #         self.filter = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
    #     self.update_table()



    def on_export_button_click(self):
        """Wird aufgerufen, wenn der Export-Button gedrückt wird."""
        messagebox.showinfo("Exportieren", "Exportieren in Arbeit")

    def on_clear_button_click(self):
        """Wird aufgerufen, wenn der Clear-Button gedrückt wird."""
        if messagebox.askyesno("Sitzung zurücksetzen?", "Tabelle leeren (Daten werden nicht gelöscht)? "):
            self.timetable.delete(*self.timetable.get_children())
            #self.filter = datetime.datetime.now()

    def on_play_button_click(self):
        """Wird aufgerufen, wenn der Play-Button gedrückt wird."""
        if self.tracker.start_time is None:
            # Erfasse die aktuelle Zeit als Startzeit und speichere sie in der JSON-Datei
            self.tracker.start()
            start_time_datetime = datetime.datetime.fromisoformat(self.tracker.start_time)
            self.timetable.insert("", "end", text=start_time_datetime.strftime("%d.%m.%y"),values=( start_time_datetime.strftime("%H:%M"),"","", ""))
            for col in self.timetable["columns"]:
                self.timetable.column(col, anchor="center")
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
            self.tracker.save()
            self.update_table()
            self.tracker.reset()
            self.play_button.config(text="Starten")
            self.play_button.config(command=self.on_play_button_click)
            

        else:
            # Der Tracker läuft nicht, also zeige eine Fehlermeldung
            tk.messagebox.showerror("Fehler", "Der Tracker läuft nicht.")


    def loadTableOnStart(self):
        """Lädt die Daten aus der JSON-Datei in die Tabelle."""
                #load all entries from the json file
        for timeRecord in reversed(self.project.get_time_records().values()):
            start_time_datetime = datetime.datetime.fromisoformat(timeRecord.start_time)
            end_time_datetime = datetime.datetime.fromisoformat(timeRecord.end_time)
            #wenn tage unterschiedlich
            if start_time_datetime.strftime("%d.%m.%y") != end_time_datetime.strftime("%d.%m.%y"):
                self.timetable.insert("", "end", text=str(start_time_datetime.strftime("%d.%m.%y")+"-"+end_time_datetime.strftime("%d.%m.%y")),values=( start_time_datetime.strftime("%H:%M"),end_time_datetime.strftime("%H:%M"),round(timeRecord.duration,1), ""))
            else:
                self.timetable.insert("", "end", text=start_time_datetime.strftime("%d.%m.%y"),values=( start_time_datetime.strftime("%H:%M"),end_time_datetime.strftime("%H:%M"),round(timeRecord.duration,1), ""))

        # center the text in the table
        for col in self.timetable["columns"]:
            self.timetable.column(col, anchor="center")


    def update_table(self):
        if self.tracker.start_time is not None:
            self.timetable.delete(*self.timetable.get_children())
            start_time_datetime = datetime.datetime.fromisoformat(self.tracker.start_time)
            end_time_datetime = datetime.datetime.fromisoformat(self.tracker.end_time)
            #wenn tage unterschiedlich
            if start_time_datetime.strftime("%d.%m.%y") != end_time_datetime.strftime("%d.%m.%y"):
                self.timetable.insert("", "end", text=str(start_time_datetime.strftime("%d.%m.%y")+"-"+end_time_datetime.strftime("%d.%m.%y")),values=( start_time_datetime.strftime("%H:%M"),end_time_datetime.strftime("%H:%M"),round(self.tracker.duration,1), ""))
            else:
                self.timetable.insert("", "end", text=start_time_datetime.strftime("%d.%m.%y"),values=( start_time_datetime.strftime("%H:%M"),end_time_datetime.strftime("%H:%M"),round(self.tracker.duration,1), ""))

        
        # center the text in the table
        for col in self.timetable["columns"]:
            self.timetable.column(col, anchor="center")


class ProjectSelection:
    def __init__(self, master):
        self.app = Application()
        self.master = master
        self.frame = tk.Frame(self.master)
        self.project_list = tk.Listbox(self.frame)
        for projectName in self.app.projects:
            self.project_list.insert("end", projectName)
        self.project_list.pack()
        self.select_button = tk.Button(self.frame, text="auswählen", command=self.on_select_button_click)
        self.select_button.pack()
        self.new_project_button = tk.Button(self.frame, text="Neues Projekt", command=self.on_new_project_button_click)
        self.new_project_button.pack()
        self.frame.pack()
        self.delete_button = tk.Button(self.frame, text="Löschen", command=self.on_delete_button_click)
        self.delete_button.pack()
        self.frame.pack()
        #add rename button
        self.rename_button = tk.Button(self.frame, text="Umbenennen", command=self.on_rename_button_click)
        self.rename_button.pack()
        self.frame.pack()
        #add label total time of all projects
        self.total_time_label = tk.Label(self.frame, text="Gesamtzeit aller Projekte: "+str(self.app.get_total_hours())+" Stunden")
        self.total_time_label.pack()


    def on_rename_button_click(self):
        if self.project_list.curselection() == ():
            tk.messagebox.showerror("Fehler", "Kein Projekt ausgewählt.")
            return
        self.rename_project_window = tk.Toplevel(self.master)
        self.rename_project_window.title("Projekt umbenennen")
        self.rename_project_window.geometry("300x100")
        self.rename_project_window.resizable(False, False)
        self.rename_project_window.grab_set()
        self.rename_project_window.focus_set()
        self.rename_project_frame = tk.Frame(self.rename_project_window)
        self.rename_project_frame.pack()
        self.rename_project_label = tk.Label(self.rename_project_frame, text="Neuer Name:")
        self.rename_project_label.pack()
        self.rename_project_entry = tk.Entry(self.rename_project_frame)
        self.rename_project_entry.pack()
        #wenn enter gedrückt wird, wird der neue name übernommen
        self.rename_project_entry.bind("<Return>", self.on_rename_project_entry_return)

    def on_rename_project_entry_return(self, event):
        self.app.rename_project(self.project_list.get(self.project_list.curselection()), self.rename_project_entry.get())
        self.project_list.delete(self.project_list.curselection())
        self.project_list.insert("end", self.rename_project_entry.get())
        self.project_list.pack()
        self.rename_project_window.destroy()


    def on_delete_button_click(self):
        if self.project_list.curselection() == ():
            tk.messagebox.showerror("Fehler", "Kein Projekt ausgewählt.")
            return
        if messagebox.askyesno("Projekt löschen?", "Projekt wirklich löschen?"):
            self.app.delete_project(self.project_list.get(self.project_list.curselection()))
            self.project_list.delete(self.project_list.curselection())
            self.project_list.pack()

        
    






    def on_new_project_button_click(self):
        print("Neues Projekt")
        """Opens a new window to create a new project."""
        self.new_project_window = tk.Toplevel(self.master)
        self.new_project_window.title("New Project")
        self.new_project_frame = tk.Frame(self.new_project_window)
        self.new_project_frame.pack()
        self.new_project_label = tk.Label(self.new_project_frame, text="Project Name:")
        self.new_project_label.pack()
        self.new_project_entry = tk.Entry(self.new_project_frame)
        self.new_project_entry.pack()                   
        self.new_project_entry.bind("<Return>", self.on_enter_pressed)
        self.new_project_entry.focus_set()



       

    def on_enter_pressed(self, event=None):
        """Creates a new project."""
        self.app.add_project(self.new_project_entry.get())
        self.new_project_window.destroy()
        #refresh the list in the selection window
        self.project_list.delete(0, "end")
        for projectName in self.app.projects:
            self.project_list.insert("end", projectName)
        


    def on_select_button_click(self):
        """Gets the selected project and closes the selection window."""
        selection = self.project_list.curselection()
        if selection:
            #get the name of the selected project
            self.selected_project = self.project_list.get(selection[0])
            self.start()
        
        else:
            messagebox.showerror("Error", "Please select a project.")

    def get_selected_project(self):
        """Returns the name of the selected project."""
        return self.selected_project

    def start(self):
        self.master.destroy()
        window = tk.Tk()
        self.app = Application()
        self.app.select_project(self.get_selected_project())
        window.title(self.get_selected_project())

        # Erstelle eine Instanz von TimeTrackerGUI und übergebe das Hauptfenster und den Tracker
        gui = Gui(window, self.app)

        # Starte die GUI
        window.mainloop()




        
    

def main():
    """Startet die GUI."""
    #startupScreen
    root = tk.Tk()
    root.title("ProjektManager")
    root.geometry("300x300")
    root.resizable(False, False)
    projectSelection = ProjectSelection(root)
    root.mainloop()


    

if __name__ == "__main__":
    main()    





