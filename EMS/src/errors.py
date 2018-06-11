class LoginError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Login error within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors


class AddGuestError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Adding guest within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors


class EventCreatingError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Event creating error within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors


class RegisterError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Register(Unregister) error within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors


class stateChangingError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "state changing error within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors


class PurchasingError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Purchasing error within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors


class cancelingError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "canceling error within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors

class closingError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "closing error within fields: %s" % (', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors

