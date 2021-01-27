import re

ip_addr_regex = r"(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])"


def find_ip_addr_in_string(string):
    '''
    Take a string and look for ip addresses within it and returns their position within it
    :param string:
    :return:
    '''
    matches = re.finditer(ip_addr_regex, string, re.MULTILINE)

    return [{
        'match': match.group(),
        'start': match.start(),
        'end': match.end()
    } for matchNum, match in enumerate(matches, start=1)]

    # print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
    #                                                                     end=match.end(), match=match.group()))
    #
    # for groupNum in range(0, len(match.groups())):
    #     groupNum = groupNum + 1
    #
    #     print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
    #                                                                     start=match.start(groupNum),
    #                                                                     end=match.end(groupNum),
    #                                                                     group=match.group(groupNum)))
