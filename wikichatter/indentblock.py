from . import indentutils as wiu
from . import signatureutils as su


# Unclean code
def generate_indentblock_list(wikicode):
    text_blocks = []
    wikicode_blocks = wiu.extract_indent_blocks(wikicode)
    continuation_indent = 0
    old_indent = 0
    for block_code in wikicode_blocks:
        local_indent = wiu.find_min_indent(block_code)
        continues = wiu.has_continuation_indent(block_code)
        if local_indent == 0 and not continues:
            continuation_indent = 0
        elif continues:
            continuation_indent = old_indent + 1
        indent = local_indent + continuation_indent
        sub_blocks = _break_block_code_by_signatures(block_code)
        for sub_block_code in sub_blocks:
            text_blocks.append(IndentBlock(sub_block_code, indent))
        old_indent = indent
    return text_blocks


def _break_block_code_by_signatures(block_code):
    sub_blocks = su.extract_signature_blocks(block_code)
    if len(sub_blocks) == 0:
        sub_blocks = [block_code]
    return sub_blocks


class IndentBlock(object):
    def __init__(self, text, indent):
        self.text = text
        self.indent = indent

    def __str__(self):
        return self.text

    def simplify(self):
        return self.text
