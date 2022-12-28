import datetime
from logging import exception
from uuid import uuid4
class TimeRecord:
    #eine uuid kann übergeben werden, muss aber nicht
    
    def __init__(self, start_time, end_time, id=None,description=""):
        if start_time != None:
            self._start_time = datetime.datetime.fromisoformat(start_time)
        else:
            self._start_time = None
        if end_time != None:
            self._end_time = datetime.datetime.fromisoformat(end_time)
        else:
            self._end_time = None
        if id == None:
            self._uuid = uuid4()
        else:
            self._uuid = id
            #convert string to uuid
            
            
        self._description = description

    @property
    def start_time(self):
        if self._start_time != None:
            return self._start_time.isoformat()
        else:
            return None

    @property
    def end_time(self):
        if self._end_time != None:
            return self._end_time.isoformat()
        else:
            return None

    @property
    def duration(self):
        try:
            return (self._end_time - self._start_time).total_seconds() / 60
        except:
            return None

    @property
    def uuid(self):
        return self._uuid.__str__()

    @property
    def description(self):
        return self._description

    def __str__(self):
        return f"Start: {self.start_time} End: {self.end_time} Duration: {self.duration}"

    @description.setter
    def description(self, description):
        if isinstance(description, str):
            self._description = description
    @start_time.setter
    def start_time(self, start_time):
        try:
            self._start_time = datetime.datetime.fromisoformat(start_time)
        except Exception as e:
            print("start_time setter",e)
            pass

    @end_time.setter
    def end_time(self, end_time):
        try:
            self._end_time = datetime.datetime.fromisoformat(end_time)
        except exception as e:
            print("end_time setter",e)
            pass

    def __eq__(self, other):
        if isinstance(other, TimeRecord):
            return self.uuid == other.uuid
        else:
            return False

    