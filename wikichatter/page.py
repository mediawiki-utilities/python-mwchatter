from . import section


class Page(object):
    def __init__(self, text, title):
        self.title = title
        self.sections = section.generate_sections_from_raw_text(text)

    def extract_comments(self, extractor):
        for s in self.sections:
            s.extract_comments(extractor)

    def simplify(self):
        basic = {"sections": [s.simplify() for s in self.sections]}
        if self.title is not None:
            basic["title"] = self.title
        return basic
