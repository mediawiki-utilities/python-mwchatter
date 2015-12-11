import WikiIndentUtils as wiu
import SignatureUtils as su


def generate_block_tree(text):
    blocks = _generate_blocks(text)
    root_node = BlockTreeNode(None,None)
    root_node.generate_block_tree(blocks)
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

class BlockTreeNode:
    def __init__(self, parent, block):
        self.parent = parent
        self.block = block
        self.children = []

    def generate_block_tree(self, block_list):
        level_block_nums = self._get_block_nums_at_start_level(block_list)
        self.children = [BlockTreeNode(self, block_list[i]) for i in level_block_nums]
        for i, child in enumerate(self.children):
            sub_start = level_block_nums[i] + 1
            if len(level_block_nums) > i+1:
                sub_end = level_block_nums[i+1]
            else:
                sub_end = len(block_list)
            child.generate_block_tree(block_list[sub_start:sub_end])

    def _get_block_nums_at_start_level(self, blocks):
        numbers = []
        if len(blocks) > 0:
            start_indent = blocks[0].indent
            for i, block in enumerate(blocks):
                    if block.indent == start_indent:
                        numbers.append(i)
        return numbers

    def __str__(self):
        spacing = ""
        self.pprint(spacing)

    def pprint(self, spacing):
        n = 100
        if self.block is not None:
            for line in self.block.text.split("\n"):
                chunks = [spacing + line[i:i+n].strip() for i in range(0, len(line), n)]
                for chunk in chunks:
                    print(chunk)
            print('\n')
        for child in self.children:
            child.pprint(spacing + "    ")
