class Session:

    __session_id = 0

    def __init__(self, name, detail, speaker, attendee_capacity):
        self._attendee_list = []
        self._id = self.generate_id()
        self._name = name
        self._detail = detail
        self._speaker = speaker
        self._attendee_capacity = attendee_capacity

    @staticmethod
    def generate_id():
        Session.__session_id += 1
        return Session.__session_id

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name

    @property
    def detail(self):
        return self._detail

    @property
    def speaker(self):
        return self._speaker

    @property
    def attendee_capacity(self):
        return self._attendee_capacity

    @property
    def attendee_list(self):
        return self._attendee_list

    def is_registered(self, email):
        for user in self.attendee_list:
            if user.email == email:
                return True
        return False

    def is_full(self):
        if len(self._attendee_list) < self._attendee_capacity:
            return False
        return True


    def add_attendee(self, user):
        self._attendee_list.append(user)


    def remove_attendee(self, user):
        self._attendee_list.remove(user)
