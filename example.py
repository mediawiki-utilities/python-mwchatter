import os
from wikichatter import TalkPageParser

talk_samples_base = "./talk_samples/"
talk_files = []
for (name, directories, files) in os.walk(talk_samples_base):
    talk_files.extend([name + "/" + f for f in files])

for f_path in talk_files:
    print("\n"*3 + f_path)
    with open(f_path, "r") as f:
        text = f.read()
        indent_tree_root = TalkPageParser.parse(text)
        print(indent_tree_root)
