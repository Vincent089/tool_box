from ciscoconfparse import CiscoConfParse


class DeviceConfigExporter(object):

    def __init__(self, config, command):
        self._command = command
        self.parsed_config = CiscoConfParse(config.splitlines())
        self._commands = self.parsed_config.find_objects('^%s' % command)

    def get_command_name(self):
        return self._commands.text[len(self._command):]

    def get_child(self, child):
        result = {child: 'not set'}

        for child_cmd in self._commands.re_search_children(r'^\s%s\s' % child):
            result[child] = child_cmd.text.strip()[len('description '):]

        return result
