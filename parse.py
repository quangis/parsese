#!/usr/bin/env python

import json
import re

if __name__ == '__main__':
    with open('./test_data.json') as f:
        questions = json.load(f)
        expression = '1.*a.*' # matches a where question with an activity.
        matcher = re.compile(expression)
        for q in questions:
            if matcher.match(q['code']):
                print(f"Question {q['id']} matched: {q['question']}?")
