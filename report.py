from collections import OrderedDict
from datetime import datetime, timedelta

import pystache

import github

TEMPLATE = r"""
{{header}}

{{#heroes}}
    {{name}}:
    {{#issues}}
        — {{ issue }}
    {{/issues}}

{{/heroes}}
"""


def get(till):
    return list(github.get_events(till))


def get_heroes():
    heroes = dict()

    for issue in get(datetime.now() - timedelta(days=1)):
        if issue['milestone'] is None or not len(issue['assignees']):
            continue

        assignees = ', '.join(issue['assignees'])
        if assignees not in heroes:
            heroes[assignees] = []

        heroes[assignees].append(issue['issue'])

    return OrderedDict(sorted(heroes.items(), key=lambda hero: len(hero[1]), reverse=True))


def get_ctx():
    heroes = list()
    for hero, issues in get_heroes().items():
        heroes.append({
            'name': hero,
            'issues': [dict(issue=issue) for issue in sorted(issues)],
        })

    return dict(heroes=heroes)


if __name__ == '__main__':
    print(pystache.render(TEMPLATE, get_ctx()))
