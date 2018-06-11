from src.user import *
from src.errors import *


class UserManager:

    @property
    def user_list(self):
        return self._userList
        
    def __init__(self):
        self._userList = []
        date = open('user.csv')
        all_data = [user for user in date]
        all_user_list = [user.split(",") for user in all_data[1:]]
        for user in all_user_list:
            user[4] = user[4][:-1]
            if user[4] == "trainee":
                self._userList.append(Student(user[0], str('z' + user[1]), user[2], user[3]))
            if user[4] == "trainer":
                self._userList.append(Staff(user[0], str('z' + user[1]), user[2], user[3]))

    def add_guest(self, name, email, password):
        errors ={}
        if email == '':
            errors['email'] = "empty email"
        else:
            for user in user_manager.user_list:
                if user.email == email:
                    errors['repeat'] = "you are not a guest"
                    break
        if name == '':
            errors['name'] = " empty name"
        if password == '':
            errors['password'] = "empty name"
        if errors != {}:
            raise AddGuestError(errors)
        else:
            new = Guest(name, email, password)
            self._userList.append(new)
