from flask_login import UserMixin
from src.event import *


class User(UserMixin, ABC):
    def __init__(self, name, zid, email, password):
        self._name = name
        self._zid = zid
        self._email = email
        self._password = password
        self._registerEventList = []

    # attribute getter
    @property
    def zid(self):
        return self._zid
        
    def get_id(self):
        return str(self._email)
        
    @property
    def is_anonymous(self):
        return False

    @property
    def name(self):
        return self._name

    @property
    def zid(self):
        return self._zid

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def registered_event_list(self):
        return self._registerEventList
        
    def get_register_seminar(self):
        seminars = []
        for event in self._registerEventList:
            if event.is_seminar() is True:
                seminars.append(event)
        return seminars

    def get_register_course(self):
        courses = []
        for event in self._registerEventList:
            if event.is_seminar() is False:
                courses.append(event)
        return courses

    # registered event list getter and remover
    # get all open registered event list
    def get_open_register_event_list(self):
        open_event = []
        for event in self._registerEventList:
            if event.status is 'open':
                open_event.append(event)
        return open_event

    # get all open registered event list
    def get_closed_register_event_list(self):
        closed_event = []
        for event in self._registerEventList:
            if event.status is 'closed':
                closed_event.append(event)
        return closed_event

    # register event list operation
    def add_register_event(self, event):
        self._registerEventList.append(event)

    def remove_register_event(self, event):
        self._registerEventList.remove(event)

    def is_registered(self, event_id):
        for event in self._registerEventList:
            if event.id == event_id:
                return True
        return False

    def get_role(self):
        pass

    def __str__(self):
        pass


# inheritance: staff and student
class Student(User):
    def __init__(self, name, zid, email, password):
        super().__init__(name, zid, email, password)

    def get_role(self):
        return "Student"

class Staff(User):
    def __init__(self, name, zid, email, password):
        super().__init__(name, zid, email, password)
        self._postedEventList = []

    @property
    def posted_event_list(self):
        return self._postedEventList

    def get_posted_seminar(self):
        seminar = []
        for event in self._postedEventList:
            if event.is_seminar() is True:
                seminar.append(event)
        return seminar

    def get_posted_course(self):
        course = []
        for event in self._postedEventList:
            if event.is_seminar() is False:
                course.append(event)
        return course

    # posted_event_list operation
    def get_open_posted_event(self):
        open_event = []
        for event in self._postedEventList:
            if event.status is 'open':
                open_event.append(event)
        return open_event

    def get_closed_posted_event(self):
        closed_event = []
        for event in self._postedEventList:
            if event.status is 'closed':
                closed_event.append(event)
        return closed_event

    def get_cancelled_posted_event(self):
        cancelled_event = []
        for event in self._postedEventList:
            if event.status is 'cancelled':
                cancelled_event.append(event)
        return cancelled_event

    def add_posted_event(self, event):
        self._postedEventList.append(event)

    def get_role(self):
        return "Staff"


class Guest(User):
    def __init__(self, name, email, password):
        super().__init__(name, None, email, password)
        self._purchased_events = []

    @property
    def purchased_events(self):
        return self._purchased_events

    def add_purchased_event(self, event):
        self._purchased_events.append(event)

    def is_purchased(self, event_id):
        for event in self._purchased_events:
            if event.id == event_id:
                return True
        return False

    def get_role(self):
        return "Guest"
