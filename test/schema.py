from jsonschema import validate


schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",

    "definitions": {
        "page": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "sections": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/section"}
                }
            }
        },
        "section": {
            "type": "object",
            "properties": {
                "heading": {"type": "string"},
                "comments": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/comment"}
                },
                "subsections": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/section"}
                }
            }
        },
        "comment": {
            "type": "object",
            "properties": {
                "author": {"type": "string"},
                "time_stamp": {"$ref": "#/definitions/time_stamp"},
                "comments": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/comment"}
                },
                "text_blocks": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/text_block"}
                },
                "cosigners": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/signature"}}
            }
        },
        "signature": {
            "type": "object",
            "properties": {
                "author": {"type": "string"},
                "time_stamp": {"$ref": "#/definitions/time_stamp"}
            }
        },
        "text_block": {
            "type": "string"
        },
        "time_stamp": {
            "type": "string",
            "pattern": "[0-9]{2}:[0-9]{2}, [0-9]{1,2} [a-zA-Z]+ [0-9]{4} \\(UTC\\)"
        }
    },

    "$ref": "#/definitions/page"
}


def verify(output):
    try:
        validate(output, schema)
        return True
    except Exception as e:
        return False


def error_msg(output):
    try:
        validate(output, schema)
        return "No error"
    except Exception as e:
        return str(e)
