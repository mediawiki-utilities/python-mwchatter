import SignatureUtils as su
import WikiIndentUtils as wiu

def get_linear_merge_comment_blocks(text):
    comment_blocks = []
    indent_blocks = wiu.extract_indent_blocks(text)
    working_block = ""
    for block in indent_blocks:
        working_block += block
        signatures = su.extract_signatures(block)
        if len(signatures) == 0:
            continue
        elif len(signatures) == 1:
            comment_blocks.append(working_block)
            working_block = ""
        else:
            comment_blocks.extend(su.extract_signature_blocks(working_block))
            working_block = ""
    return comment_blocks

def get_level_merge_comment_blocks(text):
    comment_blocks = []
    indent_blocks = wiu.extract_indent_blocks(text)
