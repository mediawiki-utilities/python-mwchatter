import SignatureUtils as su
import WikiIndentUtils as wiu

def get_likely_comment_blocks(text):
    final_blocks = []
    indent_blocks = _indent_defined_blocks(text)
    working_blocks = []
    for block in indent_blocks:
        working_blocks.append(block)
        w_block = "\n".join(working_blocks)
        signatures = su.extract_signatures(w_block)
        if len(signatures) > 1:
            final_blocks.extend(_split_on_signatures(w_block))
            working_blocks = []
        elif len(signatures) == 1:
            final_blocks.append(w_block)
            working_blocks = []
    return final_blocks


def _indent_defined_blocks(text):
    old_indent = 0
    block_list = []
    cur_block_lines = []
    for line in text.split('\n'):
        indent = wiu.find_line_indent(line)
        if indent != old_indent and line.strip() != "":
            block = "\n".join(cur_block_lines)
            block_list.append(block)
            cur_block_lines = []
            old_indent = indent
        cur_block_lines.append(line)
    block = "\n".join(cur_block_lines)
    block_list.append(block)
    return block_list

def _split_on_signatures(text):
    signatures = su.extract_signatures(text)
    # TODO
