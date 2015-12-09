
def find_min_indent(text):
    lines = text.split('\n')
    non_empty = [line for line in lines if line.strip() != ""]
    indents = [find_line_indent(line) for line in non_empty]
    return min(indents)

def find_line_indent(line):
    colons = _count_colons(line)
    stars = _count_stars(line)
    return max([colons, stars])

def _count_colons(line):
    return _count_leading_char(line, ':')

def _count_stars(line):
    return _count_leading_char(line, '*')

def _count_leading_char(line, char):
    line = line.strip()
    if len(line)==0 or line[0]!=char:
        return 0
    else:
        return 1 + _count_leading_char(line[1:], char)
