import unittest
import wikichatter.mwparsermod as mwpm
import mwparserfromhell as mwp


SECTION = ("== Heading 1 ==\n"
           "Some text\n"
           "Some other\n")
SUBSUBSECTION = ("=== Heading 1a ===\n"
                 "Some text\n"
                 "Other text\n")


class MWParserModTest(unittest.TestCase):

    def test_returns_wikicode(self):
        wikitext = SECTION

        wikicode = mwpm.parse(wikitext)

        self.assertIsInstance(wikicode, mwp.wikicode.Wikicode)

    def test_resulting_string_the_same(self):
        wikitext = (SECTION + SUBSUBSECTION + SECTION + SUBSUBSECTION)

        wikicode = mwpm.parse(wikitext)

        self.assertEqual(wikitext, str(wikicode))

    def test_sections_preserved(self):
        wikitext_list = [SECTION, SUBSUBSECTION, SECTION, SUBSUBSECTION]
        wikitext = ''.join(wikitext_list)

        wikicode = mwpm.parse(wikitext)
        other = mwp.parse(wikitext)

        detected_sections = wikicode.get_sections(flat=True)
        other_sections = other.get_sections(flat=True)
        for i, sect in enumerate(detected_sections):
            self.assertEqual(sect, str(other_sections[i]))
