import getpass


class User:
    def __str__(self):
        return '%s<%s>' % (self.__class__.__name__, self._username)

    def __init__(self, username=getpass.getuser()):
        self._username = username
        self._password = None

    def change_user(self):
        self._username = input('Enter username (default = %s) :' % getpass.getuser())

    def ask_password(self):
        self._password = getpass.getpass(prompt='Enter user password :')

    def get_user(self):
        return self._username

    def get_pwd(self):
        return self._password
