#!/usr/bin/env python

# TODO: Use the json file when it is ready.
TEST_DATA = """[
    {
        "question": "Where are the houses for sale in Utrecht",
        "id": "1",
        "source": "Competency questions",
        "title": "IAOA Summer Institute on Places and Things",
        "code": "1torn",
        "pnames": [
            "utrecht"
        ],
        "ptypes": [
            "house"
        ],
        "objects": [
            "sale"
        ],
        "activities": [],
        "situations": [],
        "qualities": [],
        "relations": [
            "in"
        ],
        "wh-words": [
            "where"
        ],
        "info": [
            {"value": "where", "type": "1"},
            {"value": "houses", "type": "t"},
            {"value": "sale", "type": "o"},
            {"value": "in", "type": "r"},
            {"value": "utrecht", "type": "n"}
        ]
    },
    {
        "question": "Where are the houses for sale and built between 1990 and 2000 in Utrecht",
        "id": "2",
        "source": "Competency questions",
        "title": "IAOA Summer Institute on Places and Things",
        "code": "1toarn",
        "pnames": [
            "utrecht"
        ],
        "ptypes": [
            "house"
        ],
        "objects": [
            "sale"
        ],
        "activities": [
            "built"
        ],
        "situations": [],
        "qualities": [],
        "relations": [
            "in"
        ],
        "wh-words": [
            "where"
        ],
        "info": [
            {"value": "where", "type": "1"},
            {"value": "houses", "type": "t"},
            {"value": "sale", "type": "o"},
            {"value": "built", "type": "a"},
            {"value": "in", "type": "r"},
            {"value": "utrecht", "type": "n"}
        ]
    }
]"""

import json
import re

if __name__ == '__main__':
    questions = json.loads(TEST_DATA)
    expression = '1.*a.*' # matches a where question with an activity.
    matcher = re.compile(expression)
    for q in questions:
        if matcher.match(q['code']):
            print(f"Question {q['id']} matched: {q['question']}?")
