from . import indentutils as wiu
from . import signatureutils as su


def generate_textblock_list(text):
    blocks = []
    indent_block_text = wiu.extract_indent_blocks(text)
    continuation_indent = 0
    old_indent = 0
    for block_text in indent_block_text:
        local_indent = wiu.find_min_indent(block_text)
        continues = wiu.has_continuation_indent(block_text)
        if local_indent == 0 and not continues:
            continuation_indent = 0
        elif continues:
            continuation_indent = old_indent + 1
        indent = local_indent + continuation_indent
        sub_blocks = _break_block_text_by_signatures(block_text)
        for sub_block_text in sub_blocks:
            blocks.append(TextBlock(sub_block_text, indent))
        old_indent = indent
    return blocks


def _break_block_text_by_signatures(text):
    sub_blocks = su.extract_signature_blocks(text)
    if len(sub_blocks) == 0:
        sub_blocks = [text]
    return sub_blocks


class TextBlock(object):
    def __init__(self, text, indent):
        self.text = text
        self.indent = indent

    def __str__(self):
        return self.text

    def simplify(self):
        return self.text
