import pprint
pp = pprint.PrettyPrinter(indent=4)

import re
import os
from wikichatter import SignatureUtils
from wikichatter import WikiIndentUtils
import mwparserfromhell as mwp
from wikichatter import WikiComments as wc
from wikichatter import TextBlocks as tb
from wikichatter import IndentTree as indT
from wikichatter import TalkPageParser

talk_samples_base = "./talk_samples/"
talk_files = []
for (name, directories, files) in os.walk(talk_samples_base):
    talk_files.extend([name + "/" +f for f in files])



sig_focused = True
for f_path in talk_files:
    print("\n"*3 + f_path)
    with open(f_path, "r") as f:
        text = f.read()
        indent_tree_root = TalkPageParser.parse(text)
        print(indent_tree_root)
