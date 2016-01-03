import mwparserfromhell as mwp
from . import section
from . import textblock
from . import comment


def extractor(text):
    text_blocks = textblock.generate_textblock_list(text)
    comments = comment.identify_comments_linear_merge(text_blocks)
    return comments


def parse(text):
    sections = section.generate_sections_from_raw_text(text)
    for s in sections:
        s.extract_comments(extractor)
    simple_sections = [s.simplify() for s in sections]
    return {"title": "", "sections": simple_sections}
