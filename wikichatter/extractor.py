from . import textblock
from . import comment


def linear_extractor(text):
    text_blocks = textblock.generate_textblock_list(text)
    comments = comment.identify_comments_linear_merge(text_blocks)
    return comments
