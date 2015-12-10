import pprint
pp = pprint.PrettyPrinter(indent=4)

import re
import os
import SignatureUtils
import WikiIndentUtils
import mwparserfromhell as mwp
import WikiComments as wc

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
    with open(f_path, "r") as f:
        text = f.read()
        wikicode = mwp.parse(text)
        sections = wikicode.get_sections()
        for section in sections:
            section_text = str(section)
            comments = wc.get_comment_blocks_linear_merge(section_text)
            for comment in comments:
                signatures = SignatureUtils.extract_signatures(comment)
                for s in signatures:
                    print(comment)
                    print( s['timestamp'] + " " + s['user'] + "\n" + s['text'])
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        # wikicode = mwp.parse(text)
        # sections = wikicode.get_sections()
        # block_marker = switch_marker()
        # for section in sections:
        #     section_text = str(section)
        #     signatures = SignatureUtils.extract_signatures(section_text)
        #     start = 0
        #     if not sig_focused:
        #         block_marker = switch_marker(block_marker)
        #     old_indent = 0
        #     for s in signatures:
        #         end = s['end']
        #         sig_text = section_text[start:end]
        #         # if "Like most integrated circuits of the" in sig_text:
        #         #     import pdb; pdb.set_trace()
        #         for line in sig_text.split('\n'):
        #             indent = WikiIndentUtils.find_line_indent(line)
        #             if old_indent != indent and line.strip() != "":
        #                 old_indent = indent
        #                 if not sig_focused:
        #                     block_marker = switch_marker(block_marker)
        #             if line.strip() != "":
        #                 print(block_marker, end="")
        #                 print(line)
        #         if sig_focused:
        #             block_marker = switch_marker(block_marker)
                #print(">>>>>>>>>>>>>>>> SigBlock block <<<<<<<<<<<<<<<<")
                # print ("===========================")
                # #print(section_text[start:end])
                # print( s['timestamp'] + " " + s['user'] + "\n" + s['text'])
                # print("Indent: {0}".format(indent))
