

# Time tracking tool

This time tracking tool allows you to track the hours worked on different projects.
## Features

- Create new projects
- Import and export projects
- Rename and delete projects
- Archive projects
- Merge projects
- Start and stop the timetracker for the current project
- Display the total working time for the current project
- Display the total working time for all projects that are not archived

## Requirements
- PyQt5
- multiplesispatch

## Installation

1. Clone the repository to your computer:
```
git clone fanse/projecTimeManager.git
```
2. Install the required dependencies:
```
pip install -r requirements.txt (not uploaded yet)
```
3. Run the program:
```
python startscreen.py
```

## Usage

- Create a new project by clicking on the "New Project" button and entering a name.
- Select the desired project from the project list.
- Click on the "Start" button to start the timetracker for the current project.
- Click on the "Stop" button to stop the timetracker for the current project.
- The time worked will automatically be added to the project.
- Use the other functions like import, export, rename, delete and archive by clicking on the corresponding buttons.

## Bugs

- [x] You can create an empty project that later becomes .json (Status: Solved)

- [ ] You can sometimes merge a project with itself, so far only on Windows (EXE) (Status: Being revised)

- [x] If the filename is too long, the file is not created, so the time is not saved (Status: Solved)

