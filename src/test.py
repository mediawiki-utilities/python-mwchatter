import pprint
pp = pprint.PrettyPrinter(indent=4)

import re
import SignatureUtils
import WikiIndentUtils

talk_samples_base = "../talk_samples/"
talk_files = []
for (name, directories, files) in os.walk(talk_samples_base):
    talk_files.extend([name + "/" +f for f in files])

pp.pprint(talk_files)

for f_path in talk_files:
    with open(f_path, "r") as f:
        text = f.read()
        signatures = SignatureUtils.extract_signatures(text)
        start = 0
        for s in signatures:
            end = s['end']
            print ("===========================")
            print(text[start:end])
            print( s['timestamp'] + " " + s['user'])
            print("Indent: {0}".format(WikiIndentUtils.find_min_indent(text[start:end])))
            start = end
