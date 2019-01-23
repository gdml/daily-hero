import time
from collections import OrderedDict
from datetime import datetime, timedelta

import requests
import schedule
from envparse import env

import github
import render

env.read_envfile()


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

        heroes[assignees].append({'number': issue['issue_number'], 'title': issue['issue_title'], 'url': issue['issue_url']})
    
    return OrderedDict(sorted(heroes.items(), key=lambda hero: len(hero[1]), reverse=True))


def get_ctx():
    heroes = list()
    for hero, issues in get_heroes().items():
        heroes.append({
            'name': hero,
            'issues': [issue for issue in sorted(issues, key=lambda issue: issue['title'])],
        })

    return dict(heroes=heroes)


def email(text, html):
    url = 'https://api.mailgun.net/v3/{}/messages'.format(env('MAILGUN_DOMAIN'))
    response = requests.post(
        url,
        auth=('api', env('MAILGUN_API_KEY')),
        data={
            'to': env('TO'),
            'from': env('FROM'),
            'subject': 'Закрытые вчера задачи',
            'text': text,
            'html': html,
        },
    )
    if response.status_code != 200:
        raise RuntimeError('Non-200 response from mailgun: {} ({})'.format(response.status_code, response.text))


def send():
    ctx = get_ctx()
    if len(ctx['heroes']):
        text = render.render_text(ctx)
        html = render.render_html(ctx)
        email(text, html)


if __name__ == '__main__':
    schedule.every().day.at('05:44').do(send)

    while True:
        schedule.run_pending()
        time.sleep(1)
