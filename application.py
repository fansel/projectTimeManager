import os
from Project import Project
import timetracker as timeTracker


class Application:
    def __init__(self):
        self.projects = {}
        self.load_projects()
        self.current_project = None
        self.current_tracker = None

    def current_project(self):
        return self.current_project
    def current_tracker(self):
        return self.current_tracker
    def projects(self):
        return self.projects


    def load_projects(self):
        project_filenames = os.listdir("./projects")
        for filename in project_filenames:
            name, _ = os.path.splitext(filename)
            project = Project(name)
            self.projects[name] = project
            print(f"Loaded project {name}")

    def add_project(self, projectname):
        self.projects[projectname] = Project(projectname)

    def rename_project(self, projectname, new_name):
        self.get_project(projectname).rename(new_name)
        self.projects[new_name] = self.projects[projectname]
        del self.projects[projectname]

    def delete_project(self, projectname):
        self.get_project(projectname).delete_file()
        del self.projects[projectname]
    def get_project(self, name):
        return self.projects.get(name)

    def get_total_hours(self):
        total_duration = 0
        for project in self.projects.values():
            total_duration += project.get_total_hours()
        return total_duration

    def select_project(self, project_name):
        project = self.get_project(project_name)
        if project:
            self.current_project = project
            self.current_tracker = timeTracker.TimeTracker(self.current_project)
        else:
            print(f"Project {project_name} not found")

    def change_current_project(self, name):
        self.current_project = self.get_project(name)
        if self.current_project is None:
            self.current_project = Project(name)
            self.add_project(self.current_project)
        print(f"Changed current project to {self.current_project.name}") 


