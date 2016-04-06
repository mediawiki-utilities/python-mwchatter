import mwparserfromhell as mwp


class Error(Exception):
    pass


class TooManyHeadingsError(Error):
    pass


EPI_LEVEL = 0


class Section(object):

    def __init__(self, wikitext):
        self._subsections = []
        self.comments = []
        self._wikicode = self._get_wikicode_from_input(wikitext)
        self._load_section_info()

    def _get_wikicode_from_input(self, wikitext):
        # wikitext can be either a wikicode object or a string
        if type(wikitext) is not mwp.wikicode.Wikicode:
            wikicode = mwp.parse(wikitext, skip_style_tags=True)
        else:
            wikicode = wikitext
        return wikicode

    def _load_section_info(self):
        wiki_headings = [h for h in self._wikicode.filter_headings()]

        if len(wiki_headings) > 1:
            raise TooManyHeadingsError(wiki_headings)
        if len(wiki_headings) == 0:
            self.heading = None
            self.level = EPI_LEVEL
        else:
            self.heading = str(wiki_headings[0].title)
            self.level = wiki_headings[0].level
        self.text = self._get_section_text_from_wikicode(self._wikicode)

    def append_subsection(self, subsection):
        self._subsections.append(subsection)

    def extract_comments(self, extractor):
        self.comments = extractor(self._wikicode)
        for s in self._subsections:
                s.extract_comments(extractor)

    def _get_section_text_from_wikicode(self, wikicode):
        sections = wikicode.get_sections(include_headings=False)
        return str(sections[-1])

    @property
    def subsections(self):
        return list(self._subsections)

    def __str__(self):
        return "<{0}: {1}>".format(self.level, self.heading)

    def __repr__(self):
        return str(self)

    def simplify(self):
        basic = {}
        basic["subsections"] = [s.simplify() for s in self._subsections]
        basic["comments"] = [c.simplify() for c in self.comments]
        if self.heading is not None:
            basic["heading"] = self.heading
        return basic


def generate_sections_from_raw_text(text):
    flat_sections = _generate_flat_list_of_sections(text)
    return _sort_into_hierarchy(flat_sections)


def _generate_flat_list_of_sections(text):
    wikicode = mwp.parse(text, skip_style_tags=True)
    mw_sections = wikicode.get_sections(include_lead=True, flat=True)
    sections = [Section(s) for s in mw_sections if len(s.nodes) > 0]
    return sections


def _sort_into_hierarchy(section_list):
    top_level_sections = []
    section_stack = []
    for section in section_list:
        while len(section_stack) > 0:
            cur_sec = section_stack[-1]
            if cur_sec.level < section.level and cur_sec.level is not EPI_LEVEL:
                cur_sec.append_subsection(section)
                section_stack.append(section)
                break
            section_stack.pop()
        if len(section_stack) is 0:
            top_level_sections.append(section)
            section_stack.append(section)
    return top_level_sections
