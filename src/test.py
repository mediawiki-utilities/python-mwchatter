import pprint
pp = pprint.PrettyPrinter(indent=4)

import re

TIMESTAMP_RE = re.compile(r"[0-9]{2}:[0-9]{2}, [0-9]{1,2} [^\W\d]+ [0-9]{4} \(UTC\)")
USER_RE = re.compile(r"(?=(\[\[User:(.*?)\|.+\]\]))", re.I)
USER_TALK_RE = re.compile(r"(?=(\[\[User talk:(.*?)\|.+\]\]))", re.I)

class Error(Exception): pass
class NoUsernameError(Error): pass
class NoTimestampError(Error): pass
class NoSignature(Error): pass

def extract_username_and_date(line):
    if not has_signature(line):
        raise NoSignature(line)
    username = extract_username(line)
    timestamp = extract_timestamp(line)
    return (username, timestamp)

def has_signature(line):
    return has_username(line) and has_timestamp(line)

def has_username(line):
    try:
        extract_username(line)
        return True
    except NoUsernameError as e:
        return False

def extract_username(line):
    names = []
    user_page_match = USER_RE.findall(line)
    user_talk_match = USER_TALK_RE.findall(line)
    if user_page_match:
        names.append(user_page_match[-1][1])
    if user_talk_match:
        names.append(user_talk_match[-1][1])
    if len(names) == 0:
        raise NoUsernameError()
    return min(names, key=len)

def has_timestamp(line):
    try:
        extract_timestamp(line)
        return True
    except NoTimestampError as e:
        return False

def extract_timestamp(line):
    match = TIMESTAMP_RE.findall(line)
    if match:
        return match[-1]
    raise NoTimestampError()

with open("../talk_samples/user/687428034.txt", "r") as f:
    lines = f.readlines()
for line in lines:
    if has_signature(line):
        (u, d) = extract_username_and_date(line)
        print(d, end=" ")
        print(u)
# pp.pprint(wikicode.get_tree())
# for node in wikicode.nodes:
#     if isinstance(node, mwp.nodes.Node):
#     #    pp.pprint(node)
#     print(type(node), end=" ")
#     pp.pprint(node)
