from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QLabel, QMessageBox, QLineEdit, QInputDialog, QMenu , QVBoxLayout, QGridLayout, QComboBox, QFileDialog,QTableWidget
from PyQt5.QtCore import Qt
from project import Project
from timerecord import TimeRecord
from timetracker import TimeTracker 
import datetime
from project_manager import ProjectManager
from stringbuilder import StringBuilder as sb
import logging
from project_selection_gui import ProjectSelection
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MainsScreen():
    """A class that creates a GUI with a Play-Pause button and a table."""
    def __init__(self,window,pm:ProjectManager):
        self.window = window
        self.pm = pm
        self.window.closeEvent = self.on_closeEvent
        self.tracker = self.pm.current_tracker
        self.project = Project(self.pm.current_project.name)
        self.progstart = datetime.datetime.now()
        self.filter = self.progstart
        self.createWidgets()
        self.createLayout()
        self.swichDropdown.setCurrentIndex(1)


        
    def createWidgets(self):
        self.createDropdown()
        self.createTable()
        self.createLabels()
        self.createButtons()
        self.createSearchBar()


    def createDropdown(self):
            self.swichDropdown = QtWidgets.QComboBox(self.window)
            self.swichDropdown.addItem("Seit Programmstart")
            self.swichDropdown.addItem("Heute")
            self.swichDropdown.addItem("Letzte Woche")
            self.swichDropdown.addItem("Letzter Monat")
            self.swichDropdown.addItem("Letztes Jahr")
            self.swichDropdown.addItem("Alle")
            self.swichDropdown.currentTextChanged.connect(self.on_dropdown)
    def createTable(self):
            # Create table
            self.timetable = QTableWidget(self.window)
            self.timetable.setColumnCount(6)
            self.timetable.setColumnHidden(4, True)
            self.timetable.setHorizontalHeaderLabels(["Datum", "Startzeit", "Endzeit", "Dauer in Minuten", "","Beschreibung"])
            self.timetable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.timetable.cellChanged.connect(self.on_entry_edit)
            #rechtsklickmenü für jede reihe erstellen
            self.timetable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.timetable.customContextMenuRequested.connect(self.on_table_right_click)
            self.timetable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.timetable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.timetable.setSortingEnabled(True)
            self.timetable.sortByColumn(0, QtCore.Qt.DescendingOrder)
            self.timetable.setAlternatingRowColors(True)
            self.timetable.setShowGrid(False)
            self.timetable.verticalHeader().setVisible(True)
            self.timetable.setCurrentCell(-1,-1)
            self.timetable.setFocusPolicy(QtCore.Qt.NoFocus)
            #if clicked outside of table, deselect all rows


        

            


        







            
            


            
            

            
            



    def createLabels(self):
        # Create label
        self.hours = QtWidgets.QLabel(self.window)
        self.hours.setText("Zeit am Projekt: " + sb.stringForTime(self.project.get_total_hours()))
    def createButtons(self):
            # Play button
            self.switch_button = QtWidgets.QPushButton(self.window)
            self.switch_button.setText("Starten")
            self.switch_button.clicked.connect(self.on_play_button_click)
            # Clear button
            self.clear_button = QtWidgets.QPushButton(self.window)
            self.clear_button.setText("Tabelle leeren")
            self.clear_button.clicked.connect(self.on_clear_button_click)
            # Back button
            self.back_button = QtWidgets.QPushButton(self.window)
            self.back_button.setText("Zurück")
            self.back_button.clicked.connect(self.on_back_button_click)
            # Export button is not needed for now
            # self.export_button = QtWidgets.QPushButton(self.window)
            # self.export_button.setText("Exportieren")
            # self.export_button.clicked.connect(self.on_export_button_click)


    def createSearchBar(self):
        self.searchBar = QtWidgets.QLineEdit(self.window)
        self.searchBar.setPlaceholderText("Suche")
        self.searchBar.setClearButtonEnabled(True)
        self.searchBar.textChanged.connect(self.on_search)
        self.searchBar.setFixedWidth(100)

    def createLayout(self):
        self.back_button.setFixedWidth(100)
        layout = QtWidgets.QVBoxLayout(self.window)
        layout.addWidget(self.back_button)        
        #search bar rechts oben
        layout.addWidget(self.searchBar)
        #position der searchbar
        layout.setAlignment(self.searchBar, QtCore.Qt.AlignmentFlag.AlignRight)
        #searchbar größe
        self.searchBar.setFixedHeight(20)
        #breite so , dass es mit der dropdown übereinstimmt
        self.searchBar.setFixedWidth(100)


        layout.addWidget(self.swichDropdown)
        layout.addWidget(self.timetable)
        layout.addWidget(self.hours)
        self.hours.setAlignment(QtCore.Qt.AlignRight)
        layout.addWidget(self.switch_button)
        layout.addWidget(self.clear_button)
        #layout.addWidget(self.export_button)



    def on_table_right_click(self, pos):
        """Opens a context menu when the user right clicks on a row."""
        if self.timetable.currentRow() == -1:
            return
        else:
            menu = QtWidgets.QMenu()
            if len(self.pm.projects) >= 2: 
                menu.addAction("zu Projekt verschieben")
            menu.addAction("löschen")
            
            if (self.timetable.currentRow() == -1 and self.timetable.currentColumn() == -1) or self.timetable.children == None:
                return
            else:
                action = menu.exec_(self.timetable.mapToGlobal(pos))
                if action == None:
                    self.timetable.clearSelection()
                    return
                if action.text() == "löschen":
                    uuid = self.timetable.item(self.timetable.currentRow(), 4).text()
                    if self.pm.current_project.get_time_record(uuid).end_time==None:
                        QMessageBox.warning(self.window, "Fehler", "Du kannst keine laufenden Aufzeichnungen löschen!")
                        return
                    delete = QtWidgets.QMessageBox.question(self.window, "Löschen", "Wirklich löschen?\nDie Dauer beträgt "+str(round(self.pm.current_project.get_time_record(uuid).duration))+" Minute(n)", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if delete == QtWidgets.QMessageBox.Yes:
                        self.pm.current_project.delete_time_record(uuid)
                        self.timetable.removeRow(self.timetable.currentRow())
                if action.text() == "zu Projekt verschieben":
                    if self.pm.current_project.get_time_record(self.timetable.item(self.timetable.currentRow(), 4).text()).end_time==None or self.tracker.is_running:
                        QMessageBox.warning(self.window, "Fehler", "Du kannst keine Aufzeichnungen verschieben während eine Aufzeichnung läuft")
                        return
                    submenu = QtWidgets.QMenu()
                    for project in self.pm.projects:
                        if project == self.pm.current_project.name:
                            continue
                        submenu.addAction(project)
                    action = submenu.exec_(self.timetable.mapToGlobal(pos))
                    if action == None:
                        return
                    self.pm.moveTimeRecord(action.text(), self.pm.current_project.get_time_record(self.timetable.item(self.timetable.currentRow(), 4).text()))
                    self.reloadTable()



    def on_dropdown(self):
                """Updates the filter attribute based on the selection in the dropdown menu."""
                value = self.swichDropdown.currentText()
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
                self.reloadTable()


    def on_search(self):
        """Filters the table based on the text in the search bar."""
        #save dropdown value
        dropdownValue = self.swichDropdown.currentIndex()
        self.swichDropdown.setCurrentIndex(5)
        text = self.searchBar.text()
        # check if parts of the text are in the table and hide the rows that don't match, ignore case
        for i in range(self.timetable.rowCount()):
            for j in range(self.timetable.columnCount()):
                if j == 4:
                    continue
                if text.lower() in self.timetable.item(i, j).text().lower():
                    self.timetable.setRowHidden(i, False)
                    break
                else:
                    self.timetable.setRowHidden(i, True)
        

    def on_closeEvent(self, event):
        if self.tracker.is_running:
            self.on_pause_button_click()
        


       


   


        

        




    
            
        



        
        

    
    def on_back_button_click(self):
        self.window.close()
        self.window = QWidget()
        self.projectselection = ProjectSelection(self.window)
        self.window.setWindowTitle("Projekt auswählen")
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window.setFocus()
        self.window.show()

    def on_clear_button_click(self):
        """Wird aufgerufen, wenn der Clear-Button gedrückt wird."""
        try:
            # Wenn   die Tabelle nicht leer ist
            if self.timetable.rowCount() > 0:
                if QMessageBox.question(None, 'Tabelle leeren', "Möchten Sie die Tabelle wirklich leeren?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No):
                    self.timetable.setRowCount(0)


                else:
                    return
        except Exception as e:
            print(e)


    def on_entry_edit(self):
        """Wird aufgerufen, wenn ein Eintrag in der Tabelle bearbeitet wird."""
        if self.timetable.currentColumn() == 5:
            uuid = self.timetable.item(self.timetable.currentRow(), 4).text()
            if uuid == self.tracker.timerecord.uuid:
                self.tracker.description = self.timetable.item(self.timetable.currentRow(), 5).text()
            else:
                self.pm.current_project.addDescriptionToUUID(uuid, self.timetable.item(self.timetable.currentRow(), 5).text())
       

        
    def reloadTable(self):
        """Loads the data from the JSON file into the table."""
        # Load all entries from the json file
        self.timetable.setRowCount(0)

        try:
            for timeRecord in self.pm.current_project.get_time_records().values():
                    start_time_datetime = datetime.datetime.fromisoformat(timeRecord.start_time)
                    end_time_datetime = datetime.datetime.fromisoformat(timeRecord.end_time)
                    # If filter is enabled, only show entries after the filter date
                    if self.filter >= start_time_datetime:
                        continue
                    if start_time_datetime.strftime("%d.%m.%y") != end_time_datetime.strftime("%d.%m.%y"):
                        self.timetable.insertRow(0)
                        self.timetable.setItem(0, 0, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%d.%m.%y") + "-" + end_time_datetime.strftime("%d.%m.%y")))
                        self.timetable.setItem(0, 1, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%H:%M")))
                        self.timetable.setItem(0, 2, QtWidgets.QTableWidgetItem(end_time_datetime.strftime("%H:%M")))
                        self.timetable.setItem(0, 3, QtWidgets.QTableWidgetItem(str(round(timeRecord.duration))))
                        self.timetable.setItem(0, 4, QtWidgets.QTableWidgetItem(timeRecord.uuid))
                        self.timetable.setItem(0, 5, QtWidgets.QTableWidgetItem(timeRecord.description))
                        

                    else:
                        self.timetable.insertRow(0)
                        self.timetable.setItem(0, 0, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%d.%m.%y")))
                        self.timetable.setItem(0, 1, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%H:%M")))
                        self.timetable.setItem(0, 2, QtWidgets.QTableWidgetItem(end_time_datetime.strftime("%H:%M")))
                        self.timetable.setItem(0, 3, QtWidgets.QTableWidgetItem(str(round(timeRecord.duration))))
                        self.timetable.setItem(0, 4, QtWidgets.QTableWidgetItem(timeRecord.uuid))
                        self.timetable.setItem(0, 5, QtWidgets.QTableWidgetItem(timeRecord.description))
                    for i in range(0, 6):
                        self.timetable.item(0, i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.hours.setText("Zeit am Projekt: " + sb.stringForTime(self.project.get_total_hours()))

        except Exception as e:
            print("Error while loading data in: " + str(e))
    def update_table(self):
            """Aktualisiert die Tabelle."""
            try:
                timeRecord=self.pm.current_project.get_LastTimeRecord()
                start_time_datetime = datetime.datetime.fromisoformat(timeRecord.start_time)
                end_time_datetime = datetime.datetime.fromisoformat(timeRecord.end_time)
                self.timetable.removeRow(0)
                if start_time_datetime.strftime("%d.%m.%y") != end_time_datetime.strftime("%d.%m.%y"):      
                    self.timetable.insertRow(0)
                    self.timetable.setItem(0, 0, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%d.%m.%y") + "-" + end_time_datetime.strftime("%d.%m.%y")))
                    self.timetable.setItem(0, 1, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%H:%M")))
                    self.timetable.setItem(0, 2, QtWidgets.QTableWidgetItem(end_time_datetime.strftime("%H:%M")))
                    self.timetable.setItem(0, 3, QtWidgets.QTableWidgetItem(str(round(timeRecord.duration))))
                    self.timetable.setItem(0, 4, QtWidgets.QTableWidgetItem(timeRecord.uuid))
                    self.timetable.setItem(0, 5, QtWidgets.QTableWidgetItem(timeRecord.description))
                else:
                    self.timetable.insertRow(0)
                    self.timetable.setItem(0, 0, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%d.%m.%y")))
                    self.timetable.setItem(0, 1, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%H:%M")))
                    self.timetable.setItem(0, 2, QtWidgets.QTableWidgetItem(end_time_datetime.strftime("%H:%M")))
                    self.timetable.setItem(0, 3, QtWidgets.QTableWidgetItem(str(round(timeRecord.duration))))
                    self.timetable.setItem(0, 4, QtWidgets.QTableWidgetItem(timeRecord.uuid))
                    self.timetable.setItem(0, 5, QtWidgets.QTableWidgetItem(timeRecord.description))
                for i in range(0, 6):
                    self.timetable.item(0, i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            except Exception as e:
                print(e)

    def on_play_button_click(self):
        """Wird aufgerufen, wenn der Play-Button gedrückt wird."""
        if self.tracker.start_time is None:
            # Erfasse die aktuelle Zeit als Startzeit und speichere sie in der JSON-Datei
            self.tracker.start()
            start_time_datetime = datetime.datetime.fromisoformat(self.tracker.start_time)
            self.timetable.insertRow(0)
            self.timetable.setItem(0, 0, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%d.%m.%y")))
            self.timetable.setItem(0, 1, QtWidgets.QTableWidgetItem(start_time_datetime.strftime("%H:%M")))
            self.timetable.setItem(0, 2, QtWidgets.QTableWidgetItem(""))
            self.timetable.setItem(0, 3, QtWidgets.QTableWidgetItem(""))
            self.timetable.setItem(0, 4, QtWidgets.QTableWidgetItem(self.tracker.timerecord.uuid))
            self.switch_button.setText("Stoppen")
            self.switch_button.clicked.disconnect()
            self.switch_button.clicked.connect(self.on_pause_button_click)
            for i in range(0, 4):
                self.timetable.item(0, i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def on_pause_button_click(self):
        """Wird aufgerufen, wenn der Pause-Button gedrückt wird."""
        if self.tracker.start_time is not None:
            # Erfasse die aktuelle Zeit als Endzeit und berechne die Dauer
            self.tracker.stop()
            self.tracker.save()
            self.update_table()
            self.update_label()
            self.tracker.reset()
            self.switch_button.setText("Starten")
            self.switch_button.clicked.disconnect()
            self.switch_button.clicked.connect(self.on_play_button_click)

            
        else:
            # Der Tracker läuft nicht, also zeige eine Fehlermeldung
            QtWidgets.QMessageBox.warning(self, "Fehler", "Der Tracker läuft nicht.")

    def update_label(self):
        """Aktualisiert die Anzeige der Gesamtzeit."""
        self.hours.setText("Zeit am Projekt: " + sb.stringForTime(self.project.get_total_hours()))