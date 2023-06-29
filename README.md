For the English version of this README, click [here](https://github.com/fansel/projectTimeManager/blob/main/README-en.md).
# Zeiterfassungstool

Dieses Zeiterfassungstool ermöglicht es, die gearbeiteten Stunden für verschiedene Projekte zu tracken.

## Funktionen

- Erstellung von neuen Projekten
- Import und Export von Projekten
- Umbenennen und Löschen von Projekten
- Archivierung von Projekten
- Zusammenführen von Projekten
- Starten und Stoppen des Timetrackers für das aktuelle Projekt
- Anzeigen der bisherigen Arbeitszeit für das aktuelle Projekt
- Anzeigen der bisherigen Arbeitszeit für alle Projekte, die nicht archiviert sind


## Voraussetzungen
- PyQt5
- multiplesispatch

## Installation

1. Klone das Repository auf deinen Computer:
```
git clone https://github.com/fansel/projecTimeManager.git
```
2. Installiere die benötigten Abhängigkeiten:
```
pip3 install -r requirements.txt (noch nicht hochgeladen)
```
3. Führe das Programm aus:
```
python3 project_selection_gui.py
```

## Verwendung

- Erstelle ein neues Projekt, indem du auf den Button "Neues Projekt" klickst und einen Namen eingibst.
- Wähle das gewünschte Projekt aus der Projektliste aus.
- Klicke auf den Button "Start", um den Timetracker für das aktuelle Projekt zu starten.
- Klicke auf den Button "Stop", um den Timetracker für das aktuelle Projekt zu stoppen. 
- Die gearbeitete Zeit wird automatisch dem Projekt hinzugefügt.
- Nutze die anderen Funktionen wie Importieren, Exportieren, Umbenennen, Löschen und Archivieren, indem du auf die entsprechenden Buttons klickst.


## Bugs 

- [x] Man kann ein leeres Projekt erstellen, welches später zu .json wird (Status: Gelöst)
- [ ] Man kann manchmal ein Projekt mit sich selbst zusammenführen, bis jetzt nur bei Windows aufgetreten (EXE) (Status: Wird überarbeitet)
- [x] Wenn der Dateiname zu lang ist, wird die Datei nicht erstellt, so dass die Zeit nicht gespeichert wird (Status: Gelöst)


