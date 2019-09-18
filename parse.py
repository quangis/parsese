#!/usr/bin/env python

import json
import re
import csv


def question_sequence_to_string(question_sequence, separator='::', brackets=('<', '>')):
    """Returns the shorthand notation of the semantically encoded question."""
    return "".join([f"{brackets[0]}{token['tag']}{separator}{token['value']}{brackets[1]}" for token in question_sequence])


def search_for_spatial_extent(relation_instance, token_code='n', print_details=False):
    expression = f'><r::{relation_instance}><{token_code}::[^>]+>$' # matches any question where relation is "in" in the relation noun pair at the end
    matcher = re.compile(expression, re.IGNORECASE)

    counter = 0
    for q in questions:
        result = matcher.search(q['shorthand'])
        if result:
            counter += 1
            if print_details:
                print(f"\tQuestion {q['id']} matched: {q['question']}?")
                print(f"\t\tMatching pattern: {result.group()}")

    if counter:
        print(f"{counter} results for spatial extent expression {expression}\n")

    return counter


def explore_spatial_extent():
    with open('spatial_extent.csv', 'w', newline='') as csvfile:
        fieldnames = ['relation', 'code', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for relation in ['of', 'in', 'within', 'for', 'by', 'per']:
            for code in codes:
                count = search_for_spatial_extent(relation, code, False)
                writer.writerow({'relation': relation, 'code': code, 'count': count})


def search_for_relation(relation_instance, token_code='n', print_details=False):
    expression = f'><r::{relation_instance}><{token_code}::[^>]+><'
    matcher = re.compile(expression, re.IGNORECASE)

    counter = 0
    for q in questions:
        result = matcher.search(q['shorthand'])
        if result:
            counter += 1
            if print_details:
                print(f"\tQuestion {q['id']} matched: {q['question']}?")
                print(f"\t\tMatching pattern: {result.group()}")

    if counter:
        print(f"{counter} results for relation expression {expression}\n")

    return counter


def explore_relation():
    with open('relation.csv', 'w', newline='') as csvfile:
        fieldnames = ['relation', 'code', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for relation in ['of', 'in', 'within', 'for', 'by', 'per']:
            for code in codes:
                count = search_for_relation(relation, code, True)
                writer.writerow({'relation': relation, 'code': code, 'count': count})


# [SC] search for any what questions that starts with a specific code (and specific instance of that code)
def search_for_what_intent(token_code='o', term_instance='[^>]+'):
    expression = f'<2::What.*<{token_code}::{term_instance}>$.*'
    matcher = re.compile(expression, re.IGNORECASE)

    with open('what_terms.csv', 'w', newline='') as csvfile:
        fieldnames = ['term']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for q in questions:
            result = matcher.search(q['intent_shorthand'])
            if result:
                writer.writerow({'term': q['intent_info'][len(q['intent_info']) - 1]['value']})
                #print(f"\tQuestion {q['id']} matched: {q['question']}?")
                #print(f"\t\tMatching pattern: {result.group()}")


def extract_what_codes():
    with open('what_codes.csv', 'w', newline='') as csvfile:
        fieldnames = ['code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for q in questions:
            if q['intent_code'].startswith('2'):
                writer.writerow({'code': q['intent_code']})


def explore_what():
    extract_what_codes()
    search_for_what_intent()

                      
if __name__ == '__main__':
    codes = list('ntoqasrpd')                  
                      
    with open('./analyzed_question.json') as f:
        questions = json.load(f)
        for q in questions:
            q['shorthand'] = question_sequence_to_string(q['all_info'])
            print(q['shorthand'])
            q['intent_shorthand'] = f"<{q['intent_code']}>{question_sequence_to_string(q['intent_info'])}"
