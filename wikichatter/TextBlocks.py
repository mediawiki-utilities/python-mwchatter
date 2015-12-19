from . import WikiIndentUtils as wiu
from . import SignatureUtils as su
from . import IndentTree

def generate_block_tree(text):
    blocks = _generate_blocks(text)
    root_node = IndentTree.IndentTreeNode(None, None)
    root_node.generate_tree_from_list(blocks)
    return root_node

def _generate_blocks(text):
    position = 0
    blocks = []
    indent_block_text = wiu.extract_indent_blocks(text)
    for block_text in indent_block_text:
        indent = wiu.find_min_indent(block_text)
        sub_blocks = _break_block_text_by_signatures(block_text)
        for sub_block_text in sub_blocks:
            blocks.append(Block(sub_block_text, position, indent))
            position += len(sub_block_text)
    return blocks

def _break_block_text_by_signatures(text):
    sub_blocks = su.extract_signature_blocks(text)
    if len(sub_blocks) == 0:
        sub_blocks = [text]
    return sub_blocks

class Block:
    def __init__(self, text, start, indent):
        self.text = text
        self.start = start
        self.indent = indent

    @property
    def end(self):
        return self.start + len(self.text)

    def __str__(self):
        return self.text
