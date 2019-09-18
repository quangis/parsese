#!/usr/bin/env python

import json
import re


def question_sequence_to_string(question_sequence, separator='::', brackets=('<', '>')):
    """Returns the shorthand notation of the semantically encoded question."""
    return "".join([f"{brackets[0]}{token['tag']}{separator}{token['value']}{brackets[1]}" for token in question_sequence])


HOW_MANY_MUCH_REGEX = re.compile(r".*<.::how (many|much)[^>]*>.*",
    flags=re.IGNORECASE)
"""
The regex matches "How many/much ...?" questions. The hypothesis is that these
questions all have *amounts* as intents (collective amounts for `many`, and 
field amounts for `much`).
"""

CAUSALITY_REGEX = re.compile(r".*(<.::affect[^>]*>|<.::effect[^>]*>|<.::influenc[^>]*>|<.::impact[^>]*>).*", flags=re.IGNORECASE)


if __name__ == '__main__':
    with open('./analyzed_question.json') as f:
        questions = json.load(f)

        for q in questions:
            q['shorthand'] = question_sequence_to_string(q['all_info'])

        with open('./hmm.txt', 'w') as f1, open('./hmm_intent_objects_types.txt', 'w') as f2:
            for q in questions:
                if HOW_MANY_MUCH_REGEX.match(q['shorthand']):
                    print(q['question'], file=f1)
                    print(" ".join([token['value'] for token in q['intent_info'] if token['tag'] in ['o', 't']]), file=f2)

        with open('./causality.txt', 'w') as f3:
            for q in questions:
                if CAUSALITY_REGEX.match(q['shorthand']):
                    print(f"\t{q['question']}?", file=f3)