import unittest
import wikichatter.section as section
import wikichatter.mwparsermod as mwpm
from wikichatter.error import MalformedWikitextError


class SectionTest(unittest.TestCase):

    def test_parses_generic_sections(self):
        wikitext = ("== Heading 1 ==\n"
                     "Some text\n"
                     "=== Heading 1a ===\n"
                     "Some text\n"
                     "== Heading 2 ==\n"
                     "Some text\n"
                     "==== Heading 2a ====\n"
                     "Some text\n"
                     "=== Heading 2b ===\n"
                     "Some text")
        wcode = mwpm.parse(wikitext)

        top_level = section.generate_sections_from_wikicode(wcode)

        self.assertEqual(len(top_level), 2, str(top_level))
        self.assertEqual(len(top_level[0].subsections), 1, top_level[0].subsections)
        self.assertEqual(len(top_level[1].subsections), 2, top_level[1].subsections)

    def test_doesnt_give_leadin_subsections(self):
        wikitext = ("Lead in text\n"
                     "=== Not a subsection ===\n"
                     "Some text\n")
        wcode = mwpm.parse(wikitext)

        top_level = section.generate_sections_from_wikicode(wcode)

        self.assertEqual(len(top_level), 2, top_level)
        self.assertEqual(len(top_level[0].subsections), 0, top_level[0].subsections)

    def test_decreasing_section_level(self):
        wikitext = ("==== Heading 1 ====\n"
                     "Some text\n"
                     "=== Heading 2 ===\n"
                     "Some text\n"
                     "== Heading 3 ==\n"
                     "Some text\n"
                     "= Heading 4 =\n"
                     "Some text\n")
        wcode = mwpm.parse(wikitext)

        top_level = section.generate_sections_from_wikicode(wcode)

        self.assertEqual(len(top_level), 4, top_level)

    def test_increasing_section_level(self):
        wikitext = ("= Heading 1 =\n"
                     "Some text\n"
                     "== Heading 2 ==\n"
                     "Some text\n"
                     "=== Heading 3 ===\n"
                     "Some text\n"
                     "==== Heading 4 ====\n"
                     "Some text\n")
        wcode = mwpm.parse(wikitext)

        top_level = section.generate_sections_from_wikicode(wcode)

        self.assertEqual(len(top_level), 1, top_level)

    def test_malformed_brackets_wikitext_raises_error(self):
        wikitext = ("= Heading 1 =\n"
                    "{{malformed|brackets]]\n\n"
                    "= Heading 2 =\n"
                    "text\n\n"
                    "= Heading 3=\n"
                    "{{}}")
        wcode = mwpm.parse(wikitext)

        with self.assertRaises(MalformedWikitextError):
            section.generate_sections_from_wikicode(wcode)
