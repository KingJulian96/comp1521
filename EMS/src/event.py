from abc import ABC
from datetime import datetime
from src.session import Session

class Event(ABC):

    __seminar_id = 0
    __course_id = 0

    def __init__(self, name, convener, details, loc, startDate, end_date, register_due_date, early_bird_date, registration_fee):
        date_format = "%Y-%m-%dT%H:%M"
        # the format of date argument is 'YEARmonthDAYhourMinute' e.g:2018-12-31T5:30
        # transform the argument into the datetime data type
        self._id = self._generate_id()
        self._name = name
        self._details = details
        self._loc = loc
        self._state = 'open'
        self._convener = convener
        self._startDate = datetime.strptime(startDate, date_format)
        self._endDate = datetime.strptime(end_date, date_format)
        self._registerDueDate = datetime.strptime(register_due_date, date_format)
        self._earlyBirdDate = datetime.strptime(early_bird_date, date_format)
        self._registration_fee = registration_fee

    @property
    def id(self):
        return self._id
        
    def _generate_id(self):
        if self.is_seminar() is True:
            Event.__seminar_id += 1
            return 'Seminar ' + str(Event.__seminar_id)
        else:
            Event.__course_id += 1
            return 'Course ' + str(Event.__course_id)

    @property
    def name(self):
        return self._name

    @property
    def details(self):
        return self._details

    @property
    def loc(self):
        return self._loc

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def convener(self):
        return self._convener

    @property
    def startDate(self):
        return self._startDate

    @property
    def end_date(self):
        return self._endDate

    @property
    def register_due_date(self):
        return self._registerDueDate

    @property
    def early_bird_date(self):
        return self._earlyBirdDate

    @property
    def registration_fee(self):
        return self._registration_fee

    def is_seminar(self):
        #return Falsue
        pass


class Seminar(Event):
    def __init__(self, name, convener, details, loc,
                 startDate, end_date, register_due_date, early_bird_date, registration_fee):
        super().__init__(name, convener, details, loc,
                         startDate, end_date, register_due_date, early_bird_date, registration_fee)
        self._sessionList = []

    @property
    def session_list(self):
        return self._sessionList

    def is_seminar(self):
        return True

    def add_session(self, name, detail, convener, attendee_capacity):
        session = Session(name, detail, convener, attendee_capacity)
        self._sessionList.append(session)

    def delete_session(self, session):
        self._sessionList.remove(session)

    def get_session(self, session_id):
        for session in self.session_list:
            if session.id == session_id:
                #break
                return session
        return None


class Course(Event):
    def __init__(self, name, convener, details, loc, startDate, end_date, register_due_date, early_bird_date, attendee_capacity, registration_fee):
        super().__init__(name, convener, details, loc, startDate, end_date, register_due_date, early_bird_date, registration_fee)
        self._presenter = convener.name
        self._attendee_capacity = int(attendee_capacity)
        self._attendee_list = []

    @property
    def presenter(self):
        return self._presenter

    @property
    def attendee_capacity(self):
        return self._attendee_capacity

    @property
    def attendee_list(self):
        return self._attendee_list

    def is_seminar(self):
        return False

    def is_full(self):
        if len(self._attendee_list) < self._attendee_capacity:
            return False
        return True

    def add_attendee(self, user):
        self._attendee_list.append(user)


    def remove_attendee(self, user):
        self._attendee_list.remove(user)
        

    def attendee_number(self):
        num = len(self._attendee_list)
        return num
