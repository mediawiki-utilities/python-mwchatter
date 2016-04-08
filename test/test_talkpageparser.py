import unittest
import wikichatter.talkpageparser as tpp
from test.schema import verify, error_msg


SECTION1 = "= Title ="
SECTION2 = "== Title =="
LEVEL0 = "Text0"
LEVEL1 = ":Text1"
LEVEL2 = "::Text2"
LEVEL3 = ":::Text3"
LEVEL4 = "::::Text4"
SIGNATURE = " [[User:Name|Name]] ([[User talk:Name|talk]]) 19:40, 18 September 2013 (UTC)"
OUTDENT = "{{outdent}}"
EL = "\n"


class TalkPageParser(unittest.TestCase):

    def test_simple_parse(self):
        text = "\n".join(
            [
                SECTION1,
                LEVEL0,
                LEVEL0 + SIGNATURE,
                LEVEL1,
                LEVEL1 + SIGNATURE,
                LEVEL2 + SIGNATURE
            ]
        )

        output = tpp.parse(text)

        self.assertTrue(verify(output), error_msg(output))
        self.assertEqual(len(output['sections']), 1)
        self.assertEqual(len(output['sections'][0]['comments']), 1)
        self.assertEqual(len(output['sections'][0]['comments'][0]['comments']), 1)

    def test_outdent_parse(self):
        text = "\n".join(
            [
                SECTION1,
                LEVEL0,
                LEVEL0 + SIGNATURE,
                LEVEL1,
                LEVEL1 + SIGNATURE,
                LEVEL2 + SIGNATURE,
                OUTDENT + LEVEL0 + SIGNATURE
            ]
        )

        output = tpp.parse(text)

        self.assertTrue(verify(output), error_msg(output))
        self.assertEqual(len(output['sections']), 1)
        self.assertEqual(len(output['sections'][0]['comments']), 1)
        self.assertEqual(len(output['sections'][0]['comments'][0]['comments']), 1)
        self.assertEqual(len(output['sections'][0]
                                   ['comments'][0]
                                   ['comments'][0]
                                   ['comments']), 1)
        self.assertEqual(len(output['sections'][0]
                                   ['comments'][0]
                                   ['comments'][0]
                                   ['comments'][0]
                                   ['comments']), 1)

    def test_multi_sections(self):
        text = "\n".join(
            [
                SECTION1,
                LEVEL0,
                LEVEL0 + SIGNATURE,
                SECTION1,
                LEVEL0,
                LEVEL0 + SIGNATURE,
            ]
        )

        output = tpp.parse(text)

        self.assertTrue(verify(output), error_msg(output))
        self.assertEqual(len(output['sections']), 2)
        self.assertEqual(len(output['sections'][0]['comments']), 1)
        self.assertEqual(len(output['sections'][1]['comments']), 1)

    def test_subsections(self):
        text = "\n".join(
            [
                SECTION1,
                LEVEL0,
                LEVEL0 + SIGNATURE,
                SECTION2,
                LEVEL0,
                LEVEL0 + SIGNATURE,
            ]
        )

        output = tpp.parse(text)

        self.assertTrue(verify(output), error_msg(output))
        self.assertEqual(len(output['sections']), 1)
        self.assertEqual(len(output['sections'][0]['comments']), 1)
        self.assertEqual(len(output['sections'][0]['subsections']), 1)
        self.assertEqual(len(output['sections'][0]['subsections'][0]['comments']), 1)
