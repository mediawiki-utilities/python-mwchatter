import os
import wikichatter as wc
import json

talk_samples_base = "./talk_samples/"
talk_files = []
for (name, directories, files) in os.walk(talk_samples_base):
    talk_files.extend([name + "/" + f for f in files])

for f_path in talk_files:
    with open(f_path, "r") as f:
        text = f.read()
        parsed = wc.parse(text)
        print(json.dumps(parsed))
