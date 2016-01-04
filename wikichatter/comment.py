from . import signatureutils as su
from . import indentutils as wiu


def identify_comments_linear_merge(text_blocks):
    working_comment = Comment()
    comments = [working_comment]
    for block in text_blocks:
        if working_comment.author is not None:
            working_comment = Comment()
            comments.append(working_comment)
        working_comment.add_text_block(block)
    return _sort_into_hierarchy(comments)


def identify_comments_level_merge(text_blocks):
    pass


def _sort_into_hierarchy(comment_list):
    top_level_comments = []
    comment_stack = []
    for comment in comment_list:
        while len(comment_stack) > 0:
            cur_com = comment_stack[-1]
            if cur_com.level < comment.level:
                cur_com.add_subcomment(comment)
                comment_stack.append(comment)
                break
            comment_stack.pop()
        if len(comment_stack) is 0:
            top_level_comments.append(comment)
            comment_stack.append(comment)
    return top_level_comments


class Error(Exception):
    pass


class MultiSignatureError(Error):
    pass


class Comment(object):

    def __init__(self):
        self.author = None
        self.time_stamp = None
        self._text_blocks = []
        self.comments = []

    def add_text_block(self, text_block):
        self._text_blocks.append(text_block)
        self.load_signature()

    def add_text_blocks(self, text_blocks):
        self._text_blocks.extend(text_blocks)
        self.load_signature()

    def add_subcomment(self, comment):
        self.comments.append(comment)

    def load_signature(self):
        signature = self._find_signature()
        if signature is not None:
            self.author = signature['user']
            self.time_stamp = signature['timestamp']

    def _find_signature(self):
        sig_list = []
        for block in self._text_blocks:
            sig_list.extend(su.extract_signatures(block.text))
        if len(sig_list) > 1:
            raise MultiSignatureError()
        if len(sig_list) == 1:
            return sig_list[0]
        else:
            return None

    @property
    def level(self):
        levels = [wiu.find_min_indent(block.text) for block in self._text_blocks]
        return min(levels)

    @property
    def text(self):
        return "\n".join([b.text for b in self._text_blocks])

    def simplify(self):
        text_blocks = [b.simplify() for b in self._text_blocks]
        comments = [c.simplify() for c in self.comments]
        return {
            "author": self.author,
            "time_stamp": self.time_stamp,
            "text_blocks": text_blocks,
            "comments": comments
        }
