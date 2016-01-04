import unittest
import wikichatter.talkpageparser as tpp
from test.schema import verify


SECTION1 = "= Title ="
SECTION2 = "== Title =="
LEVEL0 = "Text"
LEVEL1 = ":Text"
LEVEL2 = "::Text"
LEVEL3 = ":::Text"
LEVEL4 = "::::Text"
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

        self.assertTrue(verify(output))
        self.assertEqual(len(output['sections']), 1)
        self.assertEqual(len(output['sections'][0]['comments']), 1)
        self.assertEqual(len(output['sections'][0]['comments'][0]['comments']), 1)
