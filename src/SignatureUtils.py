import re

class Error(Exception): pass
class NoUsernameError(Error): pass
class NoTimestampError(Error): pass
class NoSignature(Error): pass

TIMESTAMP_RE = re.compile(r"[0-9]{2}:[0-9]{2}, [0-9]{1,2} [^\W\d]+ [0-9]{4} \(UTC\)")
USER_RE = re.compile(r"(\[\[\W*user\W*:(.*?)\|[^\]]+\]\])", re.I)
USER_TALK_RE = re.compile(r"(\[\[\W*user[_ ]talk\W*:(.*?)\|[^\]]+\]\])", re.I)
USER_CONTRIBS_RE = re.compile(r"(\[\[\W*Special:Contributions/(.*?)\|[^\]]+\]\])", re.I)

def has_signature(text):
    signatures = extract_signatures(text)
    return len(signatures) > 0

def extract_signature_blocks(text):
    blocks = []
    signatures = extract_signatures(text)
    start = 0
    for sig in signatures:
        end = _find_next_endline(text, sig['end'])
        blocks.append(text[start:end])
        start = end
    return blocks

def extract_signatures(text):
    """
    Returns all signatures found in the text as a list of dictionaries
    [
        {'user':<username>,
         'timestamp':<timestamp_as_string>,
         'text':<signature text>,
         'start':<start_location>,
         'end':<end_location>}
    ]
    """
    signature_list = []
    divided_text = _divide_on_timestamp(text)
    for (t, base_start, _) in divided_text:
        s = _try_extract_signature(t)
        if s is not None:
            s['start'] += base_start
            s['end'] += base_start
            signature_list.append(s)
    return signature_list

def _divide_on_timestamp(text):
    divided_text = []
    locations = _find_timestamp_locations(text)
    old_end = 0
    for ( _, t_end) in locations:
        end = _find_next_endline(text, t_end)
        divided_text.append((text[old_end:end], old_end, end))
        old_end = end
    return divided_text

def _find_next_endline(text, position):
    endlines = [i for i, letter in enumerate(text) if letter == '\n']
    candidates = [i for i in endlines if i >= position]
    candidates.append(len(text))
    return min(candidates)

def _try_extract_signature(text):
    try:
        return _extract_rightmost_signature(text)
    except NoSignature as e:
        return None

def _extract_rightmost_signature(text):
    try:
        (timestamp, ts_start, ts_end) = _extract_rightmost_timestamp(text)
        (user, u_start, u_end) = _extract_rightmost_user(text)
    except(NoTimestampError, NoUsernameError) as e:
        raise NoSignature(e)
    start = min(u_start, ts_start)
    end = max(u_end, ts_end)
    return {'user':user, 'timestamp':timestamp, 'text':text[start:end], 'start':start, 'end':end}

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
    uc_locs = _find_usercontribs_location(text)

    func_picker = [(l[0], l[1], _extract_userpage_user) for l in up_locs]
    func_picker.extend([(l[0], l[1], _extract_usertalk_user) for l in ut_locs])
    func_picker.extend([(l[0], l[1], _extract_usercontribs_user) for l in ut_locs])

    if len(func_picker) == 0:
        raise NoUsernameError(text)
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
    raw_username = up.group(2)
    return _clean_extracted_username(raw_username)

def _extract_usertalk_user(text):
    ut = USER_TALK_RE.match(text)
    if ut is None:
        raise NoUsernameError(text)
    raw_username = ut.group(2)
    return _clean_extracted_username(raw_username)

def _extract_usercontribs_user(text):
    uc = USER_CONTRIBS_RE.match(text)
    if uc is None:
        raise NoUsernameError(text)
    raw_username = uc.group(2)
    return _clean_extracted_username(raw_username)

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

def _find_usercontribs_location(text):
    return _find_regex_locations(USER_CONTRIBS_RE, text)

def _find_regex_locations(regex, text):
    regex_iter = regex.finditer(text)
    return [m.span() for m in regex_iter]
