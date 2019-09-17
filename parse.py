#!/usr/bin/env python

import json
import re


def question_sequence_to_string(question_sequence):
    return "".join([f"[{token['tag']}:{token['value']}]" for token in question_sequence])

if __name__ == '__main__':
    with open('./analyzed_question.json') as f:
        questions = json.load(f)
        expression = '5.*' # matches a where question with an activity.
        matcher = re.compile(expression)
        for q in questions:
            q['shorthand'] = question_sequence_to_string(q['all_info'])
            print(q['shorthand'])