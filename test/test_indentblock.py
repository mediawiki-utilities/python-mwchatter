import unittest
import wikichatter.indentblock as indentblock
import wikichatter.mwparsermod as mwpm


EMPTY = "\n"
LEVEL0 = "Level 0\n"
LEVEL1 = ":Level 1\n"
LEVEL2 = "::Level 2\n"
LEVEL3 = ":::Level 3\n"
LEVEL4 = "::::Level 4\n"

LIST1 = "*Level 1\n"
LIST2 = "**Level 2\n"
LIST3 = "***Level 3\n"
LIST4 = "****Level 4\n"

OUTDENT = "{{outdent}}"
OUTDENT_LEVEL = "{{outdent|5}}"


class IndentBlockTest(unittest.TestCase):

    def test_generates_list_from_basic_input(self):
        text = (
            LEVEL0 +
            LEVEL1 +
            LEVEL2 +
            LEVEL3
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0].indent, 0)
        self.assertEqual(blocks[1].indent, 1)
        self.assertEqual(blocks[2].indent, 2)
        self.assertEqual(blocks[3].indent, 3)

    def test_generates_list_from_reverse_input(self):
        text = (
            LEVEL3 +
            LEVEL2 +
            LEVEL1 +
            LEVEL0
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0].indent, 3)
        self.assertEqual(blocks[1].indent, 2)
        self.assertEqual(blocks[2].indent, 1)
        self.assertEqual(blocks[3].indent, 0)

    def test_generates_list_from_zigzag_input(self):
        text = (
            LEVEL0 +
            LEVEL1 +
            LEVEL2 +
            LEVEL3 +
            LEVEL2 +
            LEVEL1 +
            LEVEL0
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 7)
        self.assertEqual(blocks[0].indent, 0)
        self.assertEqual(blocks[1].indent, 1)
        self.assertEqual(blocks[2].indent, 2)
        self.assertEqual(blocks[3].indent, 3)
        self.assertEqual(blocks[4].indent, 2)
        self.assertEqual(blocks[5].indent, 1)
        self.assertEqual(blocks[6].indent, 0)

    def test_handles_outdent(self):
        text = (
            LEVEL0 +
            LEVEL1 +
            LEVEL2 +
            OUTDENT + LEVEL0
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[3].indent, 3)

    def test_handles_double_outdent(self):
        text = (
            LEVEL0 +
            LEVEL1 +
            LEVEL2 +
            OUTDENT + LEVEL0 +
            LEVEL1 +
            LEVEL2 +
            OUTDENT + LEVEL0
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 7)
        self.assertEqual(blocks[6].indent, 6)

    def test_handles_triple_outdent(self):
        text = (
            LEVEL0 +
            LEVEL1 +
            OUTDENT + LEVEL0 +
            LEVEL1 +
            OUTDENT + LEVEL0 +
            LEVEL1 +
            OUTDENT + LEVEL0
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 7)
        self.assertEqual(blocks[6].indent, 6)

    def test_generates_list_from_basic_list_input(self):
        text = (
            LEVEL0 +
            LIST1 +
            LIST2 +
            LIST3
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0].indent, 0)
        self.assertEqual(blocks[1].indent, 1)
        self.assertEqual(blocks[2].indent, 2)
        self.assertEqual(blocks[3].indent, 3)

    def test_breaks_same_level_apart(self):
        text = (
            LEVEL0 +
            LIST1 +
            LIST1 +
            LIST2 +
            LIST3
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 5)
        self.assertEqual(blocks[0].indent, 0)
        self.assertEqual(blocks[1].indent, 1)
        self.assertEqual(blocks[2].indent, 1)
        self.assertEqual(blocks[3].indent, 2)
        self.assertEqual(blocks[4].indent, 3)

    def test_grants_empty_line_previous_indent(self):
        text = (
            LEVEL0 +
            LIST1 +
            EMPTY +
            LIST1 +
            LIST2
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 5)
        self.assertEqual(blocks[0].indent, 0)
        self.assertEqual(blocks[1].indent, 1)
        self.assertEqual(blocks[2].indent, 1)
        self.assertEqual(blocks[3].indent, 1)
        self.assertEqual(blocks[4].indent, 2)


    def test_gives_empty_start_zero_indent(self):
        text = (
            EMPTY +
            LEVEL0 +
            LIST1 +
            LIST1 +
            LIST2
        )
        code = mwpm.parse(text)

        blocks = indentblock.generate_indentblock_list(code)

        self.assertEqual(len(blocks), 5)
        self.assertEqual(blocks[0].indent, 0)
        self.assertEqual(blocks[1].indent, 0)
        self.assertEqual(blocks[2].indent, 1)
        self.assertEqual(blocks[3].indent, 1)
        self.assertEqual(blocks[4].indent, 2)
