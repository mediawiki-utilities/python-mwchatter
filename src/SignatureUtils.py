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
        {'user':<username>, 'datetime':<datetime_as_datetime>, 'text':<signature text>}
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
        return _extract_rightmost_signature(text):
    except NoSignature as e:
        return None

def _extract_rightmost_signature(text):
    pass

def _find_timestamp_locations(text):
    return _find_regex_locations(TIMESTAMP_RE, text)

def _find_userpage_locations(text):
    return _find_regex_locations(USER_RE, text)

def _find_usertalk_locations(text):
    return _find_regex_locations(USER_TALK_RE, text)

def _find_regex_locations(text, regex):
    regex_iter = regex.finditer(text)
    return [m.span() for m in regex_iter]
