class Device:
    def __init__(self, hostname, os, ip, config=None):
        self.hostname = hostname
        self.os = os
        self.ip = ip
        self.config = config

    def __str__(self):
        return self.hostname
