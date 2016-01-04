from . import section


class Page(object):
    def __init__(self, text, title):
        self.title = title
        self.sections = section.generate_sections_from_raw_text(text)

    def extract_comments(self, extractor):
        for s in self.sections:
            s.extract_comments(extractor)

    def simplify(self):
        sections = [s.simplify() for s in self.sections]
        return {
            "title": self.title,
            "sections": sections
        }
