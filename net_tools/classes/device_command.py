class DeviceCommand(object):
    def __init__(self, connection, command):
        self._connection = connection
        self._command = command

    def run_command(self):
        return self._connection.execute(self._command)
