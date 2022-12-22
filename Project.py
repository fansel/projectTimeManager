import os
import json
from timerecord import TimeRecord
import shutil
from multipledispatch import dispatch

class Project:
    def __init__(self, name):
        self.name = name
        self.time_records = {}
        self.filename = os.path.join("./projects", f"{name}.json")
        self.load_time_records()

    def rename(self, new_name):
        if os.path.exists(new_name+".json"): 
           print("Project already exists")
        else:   
            newFilename = os.path.join("./projects", f"{new_name}.json")
            os.rename(self.filename, newFilename)
            self.filename = newFilename
            self.name = new_name
            print(f"Renamed project to {self.name}")


           
            
    def name(self):
        return self.name
    def create_file(self):
        if not os.path.exists("./projects"):
            os.mkdir("./projects")
            print("Created projects folder")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                print(f"Created {self.filename} file")

    def delete_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Deleted {self.filename} file")

                
    def write_time_record(self, start_time, end_time):
        time_record = TimeRecord(start_time, end_time)
        self.time_records[time_record.start_time] = time_record
        self.save_to_file()


    def save_to_file(self):
        data = []
        for start_time, time_record in self.time_records.items():
            #after each entry new line
            data.append({
                "start_time":time_record.start_time,"end_time":time_record.end_time})
        with open(self.filename, "w") as file:
            
            json.dump(data, file,indent=4)
        

    def load_time_records(self):
        tempRecords= self.time_records
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                for record in data:
                    start_time = record["start_time"]
                    end_time = record["end_time"]
                    time_record = TimeRecord(start_time, end_time)
                    self.time_records[start_time] = time_record
                return self.time_records
        except FileNotFoundError:
            self.create_file()
            self.time_records = tempRecords
            return self.time_records
        except json.decoder.JSONDecodeError:
            print("Input not valid!")
            self.time_records = tempRecords
            return self.time_records
        except Exception as e:
            print(e)

    def get_time_record(self, start_time):
        '''Returns a TimeRecord object from the project'''
        self.load_time_records()
        try:
            return self.time_records[start_time]
        except KeyError:
            return TimeRecord("","")
    def get_time_records(self):
        self.load_time_records()
        return self.time_records

    @dispatch(TimeRecord)
    def delete_time_record(self, time_record):# pyright: ignore
      self.delete_time_record(time_record.start_time)

    @dispatch(str)
    def delete_time_record(self, start_time):
        try:
            del self.time_records[start_time]
            self.save_to_file()
        except Exception as e:
            print(e)

    def get_total_hours(self):
        total_time = 0
        for time_record in self.time_records.values():
            total_time += time_record.duration
            #return total_time in minutes
        return round(total_time/ 60,1) 

    def print_time_records(self):
        for time_record in self.time_records.values():
            print(time_record)
            
    def get_LastTimeRecord(self):
        if len(self.time_records) == 0:
            return TimeRecord("","")
        else:
            return self.time_records[list(self.time_records)[-1]]
