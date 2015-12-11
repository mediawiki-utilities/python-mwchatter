import pprint
pp = pprint.PrettyPrinter(indent=4)

import re
import os
import SignatureUtils
import WikiIndentUtils
import mwparserfromhell as mwp
import WikiComments as wc
import TextBlocks as tb
import IndentTree as indT
import TalkPageParser

def switch_marker(block_marker = ""):
    if block_marker == "#### ":
        return "     "
    else:
        return "#### "

talk_samples_base = "../talk_samples/"
talk_files = []
for (name, directories, files) in os.walk(talk_samples_base):
    talk_files.extend([name + "/" +f for f in files])



sig_focused = True
for f_path in talk_files:
    print("\n"*3 + f_path + "\n"*3)
    with open(f_path, "r") as f:
        text = f.read()
        indent_tree_root = TalkPageParser.parse(text)
        print(indent_tree_root)
