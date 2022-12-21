import datetime
class TimeRecord:
    def __init__(self, start_time, end_time):
        try:      
            self._start_time = datetime.datetime.fromisoformat(start_time)
            self._end_time = datetime.datetime.fromisoformat(end_time)
            self._duration = (self._end_time - self._start_time).total_seconds() / 60
           
        except :
            self._start_time = None
            self._end_time = None
            self._duration = 0

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
        return self._duration

    def __str__(self):
        return f"Start: {self.start_time} End: {self.end_time} Duration: {self.duration}"