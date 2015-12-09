import re

class Error(Exception): pass
class NoUsernameError(Error): pass
class NoTimestampError(Error): pass
class NoSignature(Error): pass

TIMESTAMP_RE = re.compile(r"[0-9]{2}:[0-9]{2}, [0-9]{1,2} [^\W\d]+ [0-9]{4} \(UTC\)")
USER_RE = re.compile(r"(\[\[\W*user\W*:(.*?)\|[^\]]+\]\])", re.I)
USER_TALK_RE = re.compile(r"(\[\[\W*user talk\W*:(.*?)\|[^\]]+\]\])", re.I)

def has_signatures(text):
    """
    Determine if the text provided has one or more signatures
    """

def extract_signatures(text):
    """
    Returns all signatures found in the text as a list of dictionaries
    [
        {'user':<username>, 'timestamp':<timestamp_as_string>, 'text':<signature text>}
    ]
    """
    signature_list = []
    divided_text = _divide_on_timestamp(text)
    for t in divided_text:
        s = _try_extract_signature(t)
        if s is not None:
            signature_list.append(s)
    return signature_list

def _divide_on_timestamp(text):
    divided_text = []
    locations = _find_timestamp_locations(text)
    old_end = 0
    for ( _, end) in locations:
        divided_text.append(text[old_end:end])
        old_end = end
    return divided_text

def _try_extract_signature(text):
    try:
        return _extract_rightmost_signature(text)
    except NoSignature as e:
        return None

def _extract_rightmost_signature(text):
    try:
        (timestamp, ts_start, ts_end) = _extract_rightmost_timestamp(text)
        (user, u_start, u_end) = _extract_rightmost_user(text[:ts_start])
    except(NoTimestampError, NoUsernameError) as e:
        raise NoSignature(e)
    return {'user':user, 'timestamp':timestamp, 'text':text[u_start:ts_end]}

def _extract_rightmost_timestamp(text):
    ts_loc = _find_timestamp_locations(text)
    if len(ts_loc) == 0:
        raise NoTimestampError(text)
    (start, end) = max(ts_loc, key=lambda e: e[1])
    timestamp = _extract_timestamp_user(text[start:end])
    return (timestamp, start, end)

def _extract_rightmost_user(text):
    up_locs = _find_userpage_locations(text)
    ut_locs = _find_usertalk_locations(text)

    func_picker = [(l[0], l[1], _extract_userpage_user) for l in up_locs]
    func_picker.extend([(l[0], l[1], _extract_usertalk_user) for l in ut_locs])

    if len(func_picker) == 0:
        NoUsernameError(text)
    (start, end, extractor) = max(func_picker, key=lambda e: e[1])
    user = extractor(text[start:end])
    return (user, start, end)

def _extract_timestamp_user(text):
    ts = TIMESTAMP_RE.match(text)
    if ts is None:
        raise NoTimestampError(text)
    timestamp = ts.group(0)
    return timestamp

def _extract_userpage_user(text):
    up = USER_RE.match(text)
    #import pdb; pdb.set_trace()
    if up is None:
        raise NoUsernameError(text)
    last_raw_username = up.group(2)
    return _clean_extracted_username(last_raw_username)

def _extract_usertalk_user(text):
    ut = USER_TALK_RE.match(text)
    if ut is None:
        raise NoUsernameError(text)
    last_raw_username = ut.group(2)
    return _clean_extracted_username(last_raw_username)

def _clean_extracted_username(raw_username):
    parts = re.split('#|/', raw_username)
    username = parts[0]
    return username.strip()

def _find_user_locations(text):
    up = _find_userpage_locations(text)
    ut = _find_usertalk_locations(text)
    return up.extend(ut)

def _find_timestamp_locations(text):
    return _find_regex_locations(TIMESTAMP_RE, text)

def _find_userpage_locations(text):
    return _find_regex_locations(USER_RE, text)

def _find_usertalk_locations(text):
    return _find_regex_locations(USER_TALK_RE, text)

def _find_regex_locations(regex, text):
    regex_iter = regex.finditer(text)
    return [m.span() for m in regex_iter]
