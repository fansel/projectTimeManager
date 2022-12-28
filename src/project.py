import os
import json
from timerecord import TimeRecord
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

                
    def write_time_record(self, time_record: TimeRecord):
        try:
            self.time_records[time_record.uuid] = time_record
            self.save_to_file()
        except Exception as e:
            print(f"Error writing time record: {e}")
    


    def save_to_file(self):
        data = []
        for start_time, time_record in self.time_records.items():
            #after each entry new line
            if time_record.description != "":
                data.append({
                "start_time":time_record.start_time,"end_time":time_record.end_time,"uuid":time_record.uuid,"description":time_record.description})
            else:
                data.append({
                    "start_time":time_record.start_time,"end_time":time_record.end_time,"uuid":time_record.uuid})
        with open(self.filename, "w") as file:
            
            json.dump(data, file,indent=4)
        self.load_time_records()
        

    def load_time_records(self):
        tempRecords= self.time_records
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                for record in data:
                    start_time = record["start_time"]
                    end_time = record["end_time"]
                    uuid = record["uuid"]
                    if "description" in record:
                        description = record["description"]
                        time_record = TimeRecord(start_time, end_time,uuid,description)
                        self.time_records[uuid] = time_record
                    else:
                        time_record = TimeRecord(start_time, end_time,uuid)
                        self.time_records[uuid] = time_record
                return self.time_records
        except FileNotFoundError:
            self.create_file()
            self.time_records = tempRecords
            return self.time_records
        except json.decoder.JSONDecodeError:
            self.time_records = tempRecords
            return self.time_records
        except KeyError:
            print("KeyError in load_time_records")
        except Exception as e:
            print(e," in load_time_records")

    def get_time_record(self, uuid)-> TimeRecord:
        '''Returns a TimeRecord object from the project'''
        self.load_time_records()
        try:
            return self.time_records[uuid]
        except KeyError:
            return TimeRecord("","")
    def get_time_records(self):
        self.load_time_records()
        return self.time_records

    @dispatch(TimeRecord)
    def delete_time_record(self, time_record):# pyright: ignore
      self.delete_time_record(time_record.start_time)
      print("Deleted time record")

    @dispatch(str)
    def delete_time_record(self, uuid):
        try:
            del self.time_records[uuid]
            self.save_to_file()
            print("Deleted time record")
        except Exception as e:
            print(e)

    def get_total_hours(self)-> float:
        total_time = 0
        for time_record in self.time_records.values():
            if time_record.duration != None:
                total_time += time_record.duration
            else:
                continue
        return round(total_time/ 60,1) 

    def print_time_records(self):
        for time_record in self.time_records.values():
            print(time_record)
            
    def get_LastTimeRecord(self)-> TimeRecord:
        if len(self.time_records) == 0:
            return TimeRecord("","")
        else:
            return self.time_records[list(self.time_records)[-1]]

    def addDescriptionToUUID(self,uuid,description):
        self.load_time_records()
        for time_record in self.time_records.values():
            if time_record.uuid == uuid:
                time_record.description = description
                self.save_to_file()
                return
        print("No time record with that uuid found")


    def merge(self,project):
        for time_record in project.time_records.values():
            self.write_time_record(time_record)
        project.delete_file()
        self.save_to_file()
        print("Merged projects")

