def extract_indent_blocks(text):
    old_indent = 0
    block_list = []
    cur_block_lines = []
    for line in text.split('\n'):
        indent = find_line_indent(line)
        if indent != old_indent and line.strip() != "":
            block = "\n".join(cur_block_lines)
            block_list.append(block)
            cur_block_lines = []
            old_indent = indent
        cur_block_lines.append(line)
    block = "\n".join(cur_block_lines)
    block_list.append(block)
    return block_list

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
