import unittest
import mwparserfromhell as mwp
import wikichatter.indentutils as indentutils


LEVEL0 = ""
LEVEL1 = ":"
LEVEL2 = "::"
LEVEL3 = ":::"
LEVEL4 = "::::"
FILLER = "Text"
EL = "\n"
OUTDENT = "{{outdent}}"


class TestIndentUtils(unittest.TestCase):

    def test_basic_extract_indent_blocks(self):
        block0 = (
            LEVEL0 + FILLER + EL +
            EL +
            LEVEL0 + FILLER + EL
        )
        block1 = LEVEL1 + FILLER + EL
        block2 = LEVEL0 + FILLER + EL
        block3 = (
            LEVEL4 + FILLER + EL +
            EL +
            LEVEL4 + FILLER
        )
        text = (
            block0 +
            block1 +
            block2 +
            block3
        )
        wikicode = mwp.parse(text)

        blocks = indentutils.extract_indent_blocks(wikicode)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(type(blocks[0]), mwp.wikicode.Wikicode)
        self.assertIn(block0, str(blocks[0]))
        self.assertEqual(type(blocks[1]), mwp.wikicode.Wikicode)
        self.assertIn(block1, str(blocks[1]))
        self.assertEqual(type(blocks[2]), mwp.wikicode.Wikicode)
        self.assertIn(block2, str(blocks[2]))
        self.assertEqual(type(blocks[3]), mwp.wikicode.Wikicode)
        self.assertIn(block3, str(blocks[3]))

    def test_basic_find_min_indent(self):
        text = (
            LEVEL4 + FILLER + EL +
            EL +
            LEVEL4 + FILLER
        )
        wikicode = mwp.parse(text)

        indent = indentutils.find_min_indent(wikicode)

        self.assertEqual(indent, 4)

    def test_positive_has_continuation_indent(self):
        text = (
            OUTDENT + FILLER + EL +
            EL +
            FILLER
        )
        wikicode = mwp.parse(text)

        result = indentutils.has_continuation_indent(wikicode)

        self.assertTrue(result)

    def test_negative_has_continuation_indent(self):
        text = (
            FILLER + EL +
            EL +
            FILLER
        )
        wikicode = mwp.parse(text)

        result = indentutils.has_continuation_indent(wikicode)

        self.assertFalse(result)
