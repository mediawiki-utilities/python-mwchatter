import mwparserfromhell as mwp


class Error(Exception):
    pass


class TooManyHeadingsError(Error):
    pass


EPI_LEVEL = 0


class Section(object):

    def __init__(self, raw_text):
        self._raw_text = raw_text
        self._subsections = []
        self._load_fields()

    def _load_fields(self):
        wikicode = mwp.parse(self._raw_text, skip_style_tags=True)
        wiki_headings = [h for h in wikicode.filter_headings()]
        if len(wiki_headings) > 1:
            raise TooManyHeadingsError()
        if len(wiki_headings) == 0:
            self.heading = ""
            self.level = EPI_LEVEL
        else:
            self.heading = wiki_headings[0].title
            self.level = wiki_headings[0].level

    def append_subsection(self, subsection):
        self._subsections.append(subsection)

    @property
    def subsections(self):
        return list(self._subsections)

    def __str__(self):
        return "<{0}: {1}>".format(self.level, self.heading)

    def __repr__(self):
        return str(self)


def generate_sections_from_raw_text(text):
    flat_sections = _generate_flat_list_of_sections(text)
    return _sort_into_hierarchy(flat_sections)


def _generate_flat_list_of_sections(text):
    wikicode = mwp.parse(text, skip_style_tags=True)
    mw_sections = wikicode.get_sections(include_lead=True, flat=True)
    sections = [Section(str(s)) for s in mw_sections if len(str(s).strip()) > 0]
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
