import SignatureUtils as su
import WikiIndentUtils as wiu
import TextBlocks as tb

class Error(Exception): pass
class MultiSignatureError(Error): pass

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

    def add_blocks(self, blocks):
        for block in blocks:
            self.add_block(block)

    @property
    def user(self):
        return self._user

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def blocks(self):
        return list(self._blocks)

    @property
    def indent(self):
        indents = [wiu.find_min_indent(block.text) for block in self._blocks]
        return min(indents)

    def _find_signature(self):
        sig_list = []
        for block in self._blocks:
            sig_list.extend(su.extract_signatures(block.text))
        if len(sig_list) > 1:
            raise MultiSignatureError()
        if len(sig_list) == 1:
            return sig_list[0]
        else:
            return None

    def __str__(self):
        output = ""
        n = 100
        chunks = []
        for block in self._blocks:
            for line in block.text.split("\n"):
                chunks.extend([line[i:i+n].strip() for i in range(0, len(line), n)])
        chunks.extend(["\n", self.timestamp, self.user])
        return "\n".join(chunks).strip()


def get_linear_merge_comments(text):
    block_tree = tb.generate_block_tree(text)
    comments = []
    working_comment = Comment()
    for block_node in block_tree.walk():
        if block_node.block != None:
            working_comment.add_block(block_node.block)
        if working_comment.user is not None:
            comments.append(working_comment)
            working_comment = Comment()
    if len(comments) > 0:
        comments[-1].add_blocks(working_comment.blocks)
    return comments

def get_level_merge_comment_blocks(text):
    blocks = _generate_blocks(text)
    comments, unclaimed_blocks = _recursive_level_merge(blocks, 0, len(blocks))
