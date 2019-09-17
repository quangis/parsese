#!/usr/bin/env python

import json
import re


def question_sequence_to_string(question_sequence, separator=':', brackets=('[', ']')):
    """Returns the shorthand notation of the semantically encoded question."""
    return "".join([f"{brackets[0]}{token['tag']}{separator}{token['value']}{brackets[1]}" for token in question_sequence])


if __name__ == '__main__':
    with open('./analyzed_question.json') as f:
        questions = json.load(f)
        for q in questions:
            q['shorthand'] = question_sequence_to_string(q['all_info'])
            print(q['shorthand'])