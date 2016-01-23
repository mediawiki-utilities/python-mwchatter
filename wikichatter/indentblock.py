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
        text_blocks.append(IndentBlock(block_code, indent))
        old_indent = indent
    return text_blocks


class IndentBlock(object):
    def __init__(self, text, indent):
        self.text = text
        self.indent = indent

    def __str__(self):
        return self.text

    def simplify(self):
        return self.text
