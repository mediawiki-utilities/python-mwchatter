# WikiChatter #
Kevin Schiroo

This is a library currently in development to parse conversations on Wikipedia
talk pages

## Basic use ##
    import TalkPageParser as tpp

    text = open(some_talk_page).read()
    parse_tree = tpp.parse(text)
    print(parse_tree)

## Current output ##
`TalkPageParser.parse()` outputs a parse tree. The first level of this tree
will be an `IndentTree.IndentTreeNode` containing a `TalkPageParser.Page`.
The second level will be nodes containing `TalkPageParser.Section`s. Every
level down from that will contain `WikiComments.Comment`s.

The children of a node containing a comment are nodes containing the responses
to the parent comment.

## Known Problems ##
* We currently assemble comments linearly, this occasionally leads to a mis-attribution
of text. In some cases a person will reply within another person's comment. In this
case the person replying will have the text they are replying to attributed to them.
* Responses are based on indentation. On occasion a person replying will break
indentation, moving up a level. This leads their entire comment to be moved up
a level. This has specifically been observed to happen when a user inserts an
image, since attempting to indent the image may not make sense. In this cases
users commenting below them will be interpreted to be replying to the person
that broke indentation rather than the original poster.

## Running tests ##
From base directory
`python -m unittest test.<text_file>`
