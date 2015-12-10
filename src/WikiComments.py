import itertools
import SignatureUtils as su
import WikiIndentUtils as wiu

class Error(Exception): pass
class MultiSignatureError(Error): pass

class Block:
    def __init__(self, text, start, indent):
        self.text = text
        self.start = start
        self.indent = indent

    @property
    def end(self):
        return self.start + len(self.text)

class Comment:
    def __init__(self):
        self._blocks = []
        self._user = None
        self._timestamp = None

    def add_block(self, block):
        self._blocks.append(block)
        signature = self._find_signature()
        if signature is not None:
            self._user = signature['user']
            self._timestamp = signature['timestamp']

    @property
    def user(self):
        return self._user

    @property
    def timestamp(self):
        return self._timestamp

    def _find_signature(self):
        sig_list = []
        for block in blocks:
            sig_list.extend(su.extract_signatures(block.text))
        if len(sig_list) > 1:
            raise MultiSignatureError()
        if len(sig_list) == 1:
            return sig_list[0]
        else:
            return None



def get_linear_merge_comment_blocks(text):
    comment_blocks = []
    indent_blocks = wiu.extract_indent_blocks(text)
    working_block = ""
    for block in indent_blocks:
        working_block += block
        signatures = su.extract_signatures(block)
        if len(signatures) == 0:
            continue
        elif len(signatures) == 1:
            comment_blocks.append(working_block)
            working_block = ""
        else:
            comment_blocks.extend(su.extract_signature_blocks(working_block))
            working_block = ""
    return comment_blocks

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


def get_level_merge_comment_blocks(text):
    comment_blocks = []
    indent_blocks = wiu.extract_indent_blocks(text)

def recursive_level_merge(indent_blocks, start, end):
    blocks = []
    block_nums_at_level = _get_block_nums_at_start_level_between(indent_blocks, start, end)
    if len(block_nums_at_level) == 1:
        return [indent_blocks[block_nums_at_level[0]]]
    else:
        for (b_start,b_end) in _pairwise(block_nums_at_level):
            blocks, undetermined = recursive_level_merge()

    return blocks, undetermined

def _get_block_nums_at_start_level_between(blocks, start, end):
    level = wiu.find_min_indent(blocks[start])
    return _get_block_numbers_at_level_between(blocks, level, start, end)

def _get_block_numbers_at_level_between(blocks, level, start, end):
    numbers = []
    for i, block in enumerate(blocks):
        if start <= i and i < end:
            indent = wiu.find_min_indent(block)
            if indent == level:
                numbers.append(i)
    return numbers

def _seperate_by_signed_unsigned(block_list):
    pass

def _block_list_has_signature(block_list):
    for block in block_list:
        if su.has_signature(block):
            return True
    return False

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
