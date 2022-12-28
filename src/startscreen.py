from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QLabel, QMessageBox, QLineEdit, QInputDialog, QMenu , QVBoxLayout, QGridLayout, QComboBox, QFileDialog
from PyQt5.QtCore import Qt
import mainscreen as mainscreen
from project import Project
from timerecord import TimeRecord
from timetracker import TimeTracker 
import datetime
from application import Application
from stringbuilder import StringBuilder as sb
import logging
import sys
from PyQt5 import QtWidgets, QtGui, QtCore




class ProjectSelection():
    def __init__(self,master:QWidget):
        self.app = Application()
        self.frame = master
        self.project_list = QListWidget(self.frame)



    
        #sort the list
        
        #if double clicked on a project, select it
        self.project_list.itemDoubleClicked.connect(self.on_project_list_double_click) 
        #if right clicked on a project, show context menu
        self.project_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self.on_project_list_right_click)
        self.context_menu = QMenu(self.frame)
        self.context_menu.addAction("Löschen", self.on_delete_button_click)
        self.context_menu.addAction("Umbenennen", self.on_rename_button_click)
        self.context_menu.addAction("Archivieren", self.on_archive_button_click)

        self.new_project_button = QPushButton(self.frame, text="Neues Projekt")
        self.new_project_button.clicked.connect(self.on_new_project_button_click)
        self.open_archive_button = QPushButton(self.frame, text="Archiv öffnen")
        self.open_archive_button.clicked.connect(self.on_open_archive_button_click)
        self.import_button = QPushButton(self.frame, text="Importieren")
        self.import_button.clicked.connect(self.on_import_button_click)
        self.export_button = QPushButton(self.frame, text="Exportieren")
        self.export_button.clicked.connect(self.on_export_button_click)
        self.total_time_label = QLabel(self.frame, text="Zeit: "+sb.stringForTime(self.app.get_total_hours()))
        self.init_project_list()

      #knöpfe anzeigen 
        layout = QVBoxLayout()
        layout.addWidget(self.new_project_button)
        layout.addWidget(self.import_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.project_list)
        layout.addWidget(self.total_time_label)
        #make very small button for opening the archive
        layout.addWidget(self.open_archive_button)
        layout.alignment = Qt.AlignTop
        self.frame.setLayout(layout)

    def init_project_list(self):
        self.project_list.clear()
        for projectName in self.app.projects:
            self.project_list.addItem(projectName)
        self.project_list.sortItems()
        #if one project in the list, select it dont show self.context_menu.addAction("Löschen und zusammenführen", self.on_merge_project)
        if self.project_list.count() == 1:
            if len(self.context_menu.actions()) == 4:
                self.context_menu.removeAction(self.context_menu.actions()[3])
        else:
            if len(self.context_menu.actions()) == 3:
                self.context_menu.addAction("Löschen und zusammenführen", self.on_merge_project)
     
    def on_archive_button_click(self):
        """Wird aufgerufen, wenn der Archivieren-Button gedrückt wird."""
        #check if a project is selected
        if self.project_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
        self.app.archive_project(self.project_list.currentItem().text())
        self.init_project_list()


    def on_open_archive_button_click(self):
        """Wird aufgerufen, wenn der Archiv-Button gedrückt wird."""
        #open a new window with a list of archived projects
        self.archived_projects_window = QWidget()
        self.archived_projects_window_layout = QVBoxLayout()
        self.archived_projects_list = QListWidget(self.archived_projects_window)
        self.archived_projects_window.setLayout(self.archived_projects_window_layout)
        self.archived_projects_window.setWindowTitle("Archivierte Projekte")
        self.archived_projects_window.setWindowModality(Qt.ApplicationModal)
        self.archived_projects_window.show()
        #add a button to unarchive a project
        self.unarchive_button = QPushButton(self.archived_projects_window, text="wiederherstellen")
        self.archived_projects_window_layout.addWidget(self.unarchive_button)
        self.unarchive_button.clicked.connect(self.on_unarchive_button_click)
        self.loadArchiveList()
        #resize window to fit the list
        self.archived_projects_window.resize(self.archived_projects_list.sizeHintForColumn(0) + 50, self.archived_projects_list.sizeHintForRow(0) * self.archived_projects_list.count() + 50)


    def loadArchiveList(self):
        self.archived_projects_list.clear()
        self.app.load_archive_projects_names()
        for projectName in self.app.archived_projects:
            self.archived_projects_list.addItem(projectName)
        self.archived_projects_list.sortItems()
        self.archived_projects_window_layout.addWidget(self.archived_projects_list)
        

    def on_unarchive_button_click(self):
        """Wird aufgerufen, wenn der Wiederherstellen-Button gedrückt wird."""
        #check if a project is selected
        if self.archived_projects_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
        self.app.unarchive_project(self.archived_projects_list.currentItem().text())
        self.loadArchiveList()
        self.init_project_list()



    def on_import_button_click(self):
        """Wird aufgerufen, wenn der Import-Button gedrückt wird."""
        file_name = QFileDialog.getOpenFileName(self.frame, "Importieren", "", "JSON-Dateien (*.json)")
        if file_name[0] != "" and file_name[0].endswith(".json"):
            self.app.import_project(file_name[0])
            self.init_project_list()

    def on_export_button_click(self):
        """Wird aufgerufen, wenn der Export-Button gedrückt wird."""
        #check if a project is selected
        if self.project_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
        file_name = QFileDialog.getSaveFileName(self.frame, "Exportieren", "", "JSON-Dateien (*.json)")
        if file_name[0] != "" and file_name[0].endswith(".json"):
            self.app.export_project(self.project_list.currentItem().text(), file_name[0])

        
    def on_merge_project(self):
        """Wird aufgerufen, wenn der Merge-Button gedrückt wird."""


        #check if a project is selected
        if self.project_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
        #show subwindow to select the project to merge with
        self.merge_window = QWidget()
        self.merge_window.setWindowTitle("Projekt zusammenführen")
        self.merge_window.setWindowModality(Qt.ApplicationModal)
        self.merge_window.resize(300, 100)
        self.merge_window.move(300, 300)
        self.merge_window.show()
        self.merge_window_layout = QVBoxLayout()
        self.merge_window.setLayout(self.merge_window_layout)
        self.merge_window_label = QLabel(self.merge_window, text="Mit welchem Projekt soll das Projekt zusammengeführt werden?")
        self.merge_window_layout.addWidget(self.merge_window_label)
        self.merge_window_list = QListWidget(self.merge_window)
        self.merge_window_layout.addWidget(self.merge_window_list)
        self.merge_window_button = QPushButton(self.merge_window, text="Löschen und zusammenführen")
        self.merge_window_button.clicked.connect(self.on_merge_button_click)
        self.merge_window_layout.addWidget(self.merge_window_button)
        #fill the list with all projects
        for projectName in self.app.projects:
            if projectName != self.project_list.currentItem().text():
                self.merge_window_list.addItem(projectName)
        self.merge_window_list.sortItems()

    def on_merge_button_click(self):
        """Wird aufgerufen, wenn der Merge-Button gedrückt wird."""
        #check if a project is selected
        if self.merge_window_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
        self.app.merge_projects(self.merge_window_list.currentItem().text(),self.project_list.currentItem().text())
        self.init_project_list()
        self.merge_window.close()


        

    def on_project_list_double_click(self):
        self.app.select_project(self.project_list.currentItem().text())
        self.frame.close()
        self.start(self.project_list.currentItem().text())

    def on_rename_button_click(self):
        if self.project_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
            # Get the currently selected item
        selectedItem = self.project_list.currentItem()
        if selectedItem:
            # Prompt the user for a new name for the selected item
            newName, ok = QInputDialog.getText(self.project_list, 'Umbenenen', 'Neuen Namen festlegen:')
            if ok:
                #prüfe ob der name schon vergeben ist
                if newName in self.app.projects:
                    QMessageBox.critical(None, "Fehler", "Projektname bereits vergeben.")
                    return
                if newName.isspace()or newName == "":
                    QMessageBox.critical(None, "Fehler", "Projektname darf nicht leer sein.")
                    return
                if len(newName) >= 255:
                    QMessageBox.critical(None, "Fehler", "Projektname darf nicht länger als 255 Zeichen sein.")
                    return
                self.app.rename_project(selectedItem.text(),newName)
                # Update the item's text
                selectedItem.setText(newName)
                self.project_list.sortItems()




        

        

    def on_project_list_right_click(self):
        if self.project_list.currentRow() == -1:
            return
        self.context_menu.exec_(QtGui.QCursor.pos())

        







    def on_select_button_click(self):
        if self.project_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
        self.app.select_project(self.project_list.currentItem().text())
        self.frame.close()
        self.start(self.project_list.currentItem().text())


    def start(self,name):
       # öffne ein GUI fenster der Klasse Gui
        self.frame = QWidget()
        self.mainscreen = mainscreen.MainsScreen(self.frame,self.app)
        self.frame.setWindowTitle(name)
        self.frame.setFixedSize(800, 600)
        self.frame.show()

     




        



    def on_new_project_button_click(self):
        newName, ok = QInputDialog.getText(self.project_list, 'Erstellen', 'Neuen Namen festlegen:')
        if ok:
            if newName in self.app.projects:
                QMessageBox.critical(None, "Fehler", "Projektname bereits vergeben.")
                return
            elif newName.isspace() or newName == "":
                QMessageBox.critical(None, "Fehler", "Projektname darf nicht leer sein.")
                return
            elif len(newName) >= 200:
                QMessageBox.critical(None, "Fehler", "Projektname darf nicht länger als 255 Zeichen sein.")
                return
            elif newName in self.app.projects:
                QMessageBox.critical(None, "Fehler", "Projektname bereits vorhanden.")
            else:
                self.app.add_project(newName)
                self.init_project_list()





    def on_new_project_entry_return(self):
        self.app.add_project(self.new_project_entry.text())
        self.project_list.addItem(self.new_project_entry.text())
        self.new_project_window.close()



    def on_delete_button_click(self):
        if self.project_list.currentRow() == -1:
            QMessageBox.critical(None, "Fehler", "Kein Projekt ausgewählt.")
            return
        if QMessageBox.question(None, "Projekt löschen?", "Projekt wirklich löschen?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
          
            self.app.delete_project(self.project_list.currentItem().text())
            self.init_project_list()

            self.total_time_label.setText("Zeit: "+sb.stringForTime(self.app.get_total_hours()))



    


def main():
        app = QApplication(sys.argv)
        #set application icon
        #set application name
        app.setApplicationName("Zeiterfassung")
        #set application version
        app.setApplicationVersion("1.0")
        #app style fusion
        app.setStyle("Fusion")
        #immer hellles theme
        app.setPalette(QApplication.style().standardPalette())
        app.setWindowIcon(QtGui.QIcon('icon.jpeg'))
        window = QWidget()
        window.setWindowTitle("Projekt auswählen")
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        window.setFocus()
        project_selection = ProjectSelection(window)
        #größe an knöpfe anpassen
        window.setFixedSize(220, 330)
        window.show()
        sys.exit(app.exec_())

    
    

if __name__ == "__main__":
    main()
