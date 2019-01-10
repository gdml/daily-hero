import time
from collections import OrderedDict
from datetime import datetime, timedelta

import pystache
import requests
import schedule
from envparse import env

import github

env.read_envfile()

TEMPLATE = r"""
{{#heroes}}
    {{name}}:
    {{#issues}}
        — {{ issue }}
    {{/issues}}

{{/heroes}}

Ваш гитхаб
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


def email(text):
    url = 'https://api.mailgun.net/v3/{}/messages'.format(env('MAILGUN_DOMAIN'))
    response = requests.post(
        url,
        auth=('api', env('MAILGUN_API_KEY')),
        data={
            'to': env('TO'),
            'from': env('FROM'),
            'subject': 'Закрытые вчера задачи',
            'text': text,
        },
    )
    if response.status_code != 200:
        raise RuntimeError('Non-200 response from mailgun: {} ({})'.format(response.status_code, response.text))


def send():
    ctx = get_ctx()
    if len(ctx['heroes']):
        email(pystache.render(TEMPLATE, ctx))


if __name__ == '__main__':
    schedule.every().day.at('08:44').do(send)

    while True:
        schedule.run_pending()
        time.sleep(1)
