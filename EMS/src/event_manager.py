from src.event import *
from src.errors import *

class EventManager:
    def __init__(self):
        self._event_List = []

    @property
    def event_list(self):
        return self._event_List

    def add_event(self, event):
        self._event_List.append(event)
        
    def romove_event(self, event):
        self._eventList.remove(event)

    def get_event(self, _id):
        for tmep in self._event_List:
            if tmep.id == _id:
                return tmep
        return None
