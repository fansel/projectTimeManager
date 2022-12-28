from datetime import datetime
from json import load
from multiprocessing.spawn import old_main_modules
import os
from typing import Dict
from project import Project
import logging
import shutil

from timetracker import TimeTracker 


class Application:
    def __init__(self):


        self.projects:Dict[str, Project] = {}
        self.archived_projects=[]
        self.load_projects()
        self.load_archive_projects_names()
        





        self.current_tracker:TimeTracker
        self.current_project:Project

    def current_tracker(self)-> TimeTracker:
        return self.current_tracker
    def current_project(self)-> Project:
        return self.current_project

    def load_projects(self):
        self.projects = {}
        if not os.path.exists("./projects"):
            os.mkdir("./projects")
            print("Created projects folder")
        project_filenames = os.listdir("./projects")
        for filename in project_filenames:
            if not filename.endswith(".json"):
                continue
            name, _ = os.path.splitext(filename)
            project = Project(name)
            self.projects[name] = project 

    def load_archive_projects_names(self):
        self.archived_projects=[]
        if not os.path.exists("./archive"):
            os.mkdir("./archive")
            print("Created archive folder")
        project_filenames = os.listdir("./archive")
        for filename in project_filenames:
            if not filename.endswith(".json"):
                continue
            name, _ = os.path.splitext(filename)
            self.archived_projects.append(name)

    def add_project(self, name):
        self.projects[name] = Project(name)

    def rename_project(self, name:str, new_name: str):
        self.get_project(name).rename(new_name)
        self.projects[new_name] = self.projects[name]
        del self.projects[name]

    def delete_project(self, projectname):
        self.get_project(projectname).delete_file()
        self.load_projects()

    def get_project(self, name:str)-> Project:
        return self.projects.get(name)


    def get_total_hours(self):
        total_duration = 0
        for project in self.projects.values():
            total_duration += project.get_total_hours()
        return total_duration

    def select_project(self, project_name: str):
        project = self.get_project(project_name)
        if project:
            self.current_project = project
            self.current_tracker = TimeTracker(self.current_project)
        else:
            print(f"Project {project_name} not found")

    def change_current_project(self, name):
        self.current_project = self.get_project(name)
        if self.current_project is None:
            self.current_project = Project(name)
            self.add_project(self.current_project)
        print(f"Changed current project to {self.current_project.name}") 



    def import_project(self, filename):
        if not os.path.exists(filename):
            print(f"File {filename} not found")
            return
        if os.path.exists(os.path.join("./projects", os.path.basename(filename))):
            print(f"File {filename} already exists in projects folder")
            return
        try:
            #copy file to projects folder using shutil
            shutil.copy(filename, "./projects")
            #get name of file
            name, _ = os.path.splitext(filename)
            #get name of file
            name = os.path.basename(name)
            #create project
            project = Project(name)
            #add project to projects
            self.projects[name] = project
            print(f"Imported project {name}")
        except Exception as e:
            print(f"Error importing project: {e}")
            
    def export_project(self, project_name, filename):
        project = self.get_project(project_name)
        if project is None:
            print(f"Project {project_name} not found")
            return
        if os.path.exists(filename):
            print(f"File {filename} already exists")
            return
        try:
            shutil.copy(project.filename, filename)
            print(f"Exported project {project_name} to {filename}")
        except Exception as e:
            print(f"Error exporting project: {e}")

    def moveTimeRecord(self, project_name, time_record):
        project = self.get_project(project_name)
        if project is None:
            print(f"Project {project_name} not found")
            return
        project.write_time_record(time_record)
        self.current_project.delete_time_record(time_record.uuid)
        print(f"Moved time record {time_record} to project {project_name}")

    def merge_projects(self, project_name, project_name2):
        project = self.get_project(project_name)
        project2 = self.get_project(project_name2)
        if project_name == project_name2:
            return
        if project is None:
            print(f"Project {project_name} not found")
            return
        if project2 is None:
            print(f"Project {project_name2} not found")
            return
        project.merge(project2)
        self.delete_project(project_name2)


    def archive_project(self, project_name):
        project = self.get_project(project_name)
        if project is None:
            print(f"Project {project_name} not found")
            return
        if not os.path.exists("./archive"):
            os.mkdir("./archive")
            print("Created archive folder")
        old_name=project_name
        if os.path.exists("./archive/"+project_name+".json"):
            i = 1
            while os.path.exists("./archive/"+project_name+str(i)+".json"):
                i += 1
            project_name += str(i)
        shutil.move("./projects/"+old_name+".json", "./archive/"+project_name+".json")
        self.delete_project(old_name)
        print(f"Archived project {project_name}")

    def unarchive_project(self, project_name):
        if project_name+".json" not in os.listdir("./archive"):
            print(f"Project {project_name} not found")
            return
        else: 
            if not os.path.exists("./projects"):
                os.mkdir("./projects")
                print("Created projects folder")
            old_name = project_name
            if os.path.exists("./projects/"+project_name+".json"):
                i = 1
                while os.path.exists("./projects/"+project_name+str(i)+".json"):
                    i += 1
                project_name += str(i)
            shutil.move("./archive/"+old_name+".json", "./projects/"+project_name+".json")
            self.load_projects()
            print(f"Unarchived project {project_name}")
            self.load_archive_projects_names()
    




