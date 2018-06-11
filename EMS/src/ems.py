from src.user_manager import *
from src.event_manager import *
from src.errors import *
#import datetime
import time
from datetime import datetime


class EMS:
    def __init__(self):
        self._userManager = UserManager()
        self._eventManager = EventManager()

    @property
    def user_manager(self):
        return self._userManager

    @property
    def event_manager(self):
        return self._eventManager
    
    # checking whether login info is valid
    def check_login(self, email, password):
        errors = {}
        if email == '':
            errors['email'] = "empty email"
        if password == '':
            errors['password'] = "empty password"
        if errors != {}:
            raise LoginError(errors)
        else:
            for user in self.user_manager.user_list:
                if user.email == email:
                    if user.password == password:
                        return user
        return None

    def all_open_seminars(self):
        seminars_list = []
        for event in self._eventManager.event_list:
            if event.is_seminar() is True:
                if event.state == 'open':
                    seminars_list.append(event)
        return seminars_list

    def all_open_courses(self):
        courses_list = []
        for event in self._eventManager.event_list:
            if event.is_seminar() is False:
                if event.state == 'open':
                    courses_list.append(event)
        return courses_list
        
    @staticmethod
    def register_session(user, seminar, session_id):
        session = seminar.get_session(session_id)

        if seminar in user.registered_event_list:
            pass
        if seminar not in user.registered_event_list:      
            user.add_register_event(seminar)
            session.add_attendee(user)
    # register operation
    # register an event by an user
    # 1. determine whether this user had already submitted the event
    # 2. determine whether this event is full
    # 3. the user cannot be convener
    # 4. the event must be opening
    # -> add user to event_attendee_list
    # -> add event to user_register_event_list
    @staticmethod
    def unregister_s(user, seminar, session_id):
        session = seminar.get_session(session_id)
        errors = {}
        if session not in seminar.session_list:
            errors['seminar'] = "no such seminar"
        if seminar.state != 'open':
            errors['state'] = "no such open seminar"
        if datetime.now() > seminar.register_due_date:
            errors['period'] = "late to register"
        if errors != {}:
            raise RegisterError(errors)
        else:
            delete_flag = True
            session.remove_attendee(user)
            for ses in seminar.session_list:
                if user in ses.attendee_list:
                    delete_flag = False
                    break
            if delete_flag:
                user.remove_register_event(seminar)
                
    @staticmethod
    def unregister_event(user, event):
        if user not in event.attendee_list:
            return False
        if event.register_due_date < datetime.now():
            return False
        event.remove_attendee(user)
        user.remove_register_event(event)

    @staticmethod
    def register_course(user, course):
        errors = {}
        errors = check_register_course_error(user, course)
        if user is course.convener:
            errors['user'] = "attendee cannot be speaker"
        if course.state != 'open':
            errors['state'] = "no such opening course"
        if course in user.registered_event_list:
            errors['repeated_register'] = "repeated registertion"
        if course.is_full() == 'True':
            errors['full'] = "the course is full"
        if errors != {}:
            raise RegisterError(errors)
        else:
            course.add_attendee(user)
            user.add_register_event(course)

    @staticmethod
    def unregister_course(user, course):
        errors = {}
        if course.state != 'open':
            errors['state'] = "no such opening course"
        if course not in user.registered_event_list:
            errors['course'] = "no registertion"
        if datetime.now() > course.register_due_date:
            errors['period'] = "late registertion"
        if errors != {}:
            raise RegisterError(errors)
        else:
            course.remove_attendee(user)
            user.remove_register_event(course)
    
    @staticmethod
    def create_event(self, user, event):
        self._eventManager.add_event(event)
        user.add_posted_event(event)
        print(ems.event_manager.event_list)
        
    @staticmethod
    def get_user_by_id(self, user_id):
        for i in self._userManager.user_list:
            if i.id == user_id:
                return i
        return None
    
    def create_course(self, name, convener, details, loc, startDate, end_date, due_date, early_bird, attendee_capacity, fee):
        errors = {}
        start = end = register_due = early_bird_day = None
        
        try:
            start = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors['startDate'] = "invalid start date"
        try:
            end = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")
        except ValueError:
            errors['end_date'] = "invalid end date"
        try:
            register_due = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors['register_due_date'] = "invalid register due date"
        try:
            early_bird_day = datetime.strptime(early_bird, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors['early_bird_date'] = "invalid early bird date"
        
        if name == '':
            errors['name'] = "name cannot be empty"
        if convener == '':
            errors['convener'] = "convener cannot be empty"
        if loc == '':
            errors['loc'] = "venue cannot be empty"
        if startDate == '':
            errors['startDate'] = "start date cannot be empty"
        if end_date == '':
            errors['end_date'] = "end date cannot be empty"
        if due_date == '':
            errors['due_date'] = "due date cannot be empty"
        if early_bird_day == '':
            errors['early_bird'] = "early bird date cannot be empty"
        if attendee_capacity == '':
            errors['attendee_capacitye'] = "attendee capacity cannot be empty"
        if fee == '':
            errors['fee'] = "guest fee cannot be empty but can be 0"
        
        if 'startDate' not in errors:
            if start < datetime.now():
                errors['period1'] = "start date must be after the current date"

        if 'startDate' not in errors and 'end_date' not in errors and 'register_due_date' not in errors:
            if register_due < start or register_due > end:
                errors['period2'] = "Register due date must be between the start date and end date"

        if 'startDate' not in errors and 'end_date' not in errors and 'early_bird_date' not in errors:
            if early_bird_day < start or early_bird_day > end:
                errors['period3'] = "Early bird date must be between the start date and end date"
        
        if 'startDate' not in errors and 'end_date' not in errors:
            if start >= end:
                errors['period4'] = "Start date must before the end date"
                
        if errors != {}:
            raise EventCreatingError(errors)
        else:
            course = Course(name, convener, details, loc, startDate, end_date,
                            due_date, early_bird, attendee_capacity, fee)
            self._eventManager.add_event(course)
            convener.add_posted_event(course)
            return course.id

    def create_seminar(self, name, convener, details, loc, startDate, end_date, due_date, early_bird, fee):
        errors = {}
        start = end = register_due = early_bird_day = None
        
        try:
            start = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors['startDate'] = "invalid start date"
        try:
            end = datetime.strptime(end_date,"%Y-%m-%dT%H:%M")
        except ValueError:
            errors['end_date'] = "invalid end date"
        try:
            register_due = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors['register_due_date'] = "invalid register due date"
        try:
            early_bird_day = datetime.strptime(early_bird, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors['early_bird_date'] = "invalid early bird date"
        
        if name == '':
            errors['name'] = "name cannot be empty"
        if convener == '':
            errors['convener'] = "convener cannot be empty"
        if loc == '':
            errors['loc'] = "venue cannot be empty"
        if startDate == '':
            errors['startDate'] = "start date cannot be empty"
        if end_date == '':
            errors['end_date'] = "end date cannot be empty"
        if due_date == '':
            errors['due_date'] = "due date cannot be empty"
        if early_bird_day == '':
            errors['early_bird'] = "early bird date cannot be empty"
        if attendee_capacity == '':
            errors['attendee_capacitye'] = "attendee capacity cannot be empty"
        if fee == '':
            errors['fee'] = "guest fee cannot be empty but can be 0"
        
        if 'startDate' not in errors:
            if start < datetime.now():
                errors['period1'] = "start date must be after the current date"

        if 'startDate' not in errors and 'end_date' not in errors and 'register_due_date' not in errors:
            if register_due < start or register_due > end:
                errors['period2'] = "Register due date must be between the start date and end date"

        if 'startDate' not in errors and 'end_date' not in errors and 'early_bird_date' not in errors:
            if early_bird_day < start or early_bird_day > end:
                errors['period3'] = "Early bird date must be between the start date and end date"
        
        if 'startDate' not in errors and 'end_date' not in errors:
            if start >= end:
                errors['period4'] = "Start date must before the end date"
        if errors != {}:
            raise EventCreatingError(errors)
        else:
            seminar = Seminar(name, convener, details, loc, startDate, end_date, due_date, early_bird, fee)
            self._eventManager.add_event(seminar)
            convener.add_posted_event(seminar)
            return seminar.id

    @staticmethod
    def create_session(seminar, name, detail, user, attendee_capacity):
        errors = {}
        if name == '':
            errors['name'] = "Name cannot be empty"
        if detail == '':
            errors['detail'] = "Detail cannot be empty"
        if speaker is None:
            errors['speaker'] = "no such speaker"
        if attendee_capacity < 1:
            errors['attendee_capacity'] = "attendee capacity must be bigger than 1"
        if errors != {}:
            raise EventCreatingError(errors)
        else:
            seminar.add_session(name, detail, user, attendee_capacity)

    @staticmethod
    def event_price(event, user):
        if event.is_seminar():
            if user.get_role() == 'Guest':
                for session in event.session_list:
                    if session.convener is user:
                        return 0
        if datetime.now() > event.early_bird:
            fee = event.fee
        else:
            fee = event.fee/2
        return fee



    def check_email(self, email):
        for user in self.user_manager.user_list:
            if user.email == email:
                return user
        return None

    @staticmethod
    def purchase_event(user, event):
        errors = {}
        if user.get_role != 'Guest':
            errors['role'] = "not a guest"
        elif user.is_purchased(event.id):
            errors['repeated'] = 'repeated purchash'
        if errors != {}:
            raise PurchasingError(errors)
        user.add_purchased_event(event)
        
    @staticmethod
    def cancel_event(user, event):
        errors = {}
        if user is not event.convener:
            errors['convener'] = 'The user is not the convener'
        if event.state != 'open':
            errors['state'] = "The event is not opening"
        if errors != {}:
            raise cancelingError(errors)
        else:   
            event.state = "cancel"

    @staticmethod
    def close_event(user, event):
        errors = {}
        if user is not event.convener:
            errors['convener'] = 'The user is not the convener'
        if event.state != 'open':
            errors['state'] = "The event can't be closed"
        if errors != {}:
            raise closingError(errors)
        else:   
            event.state = "close"

