import re
from datetime import datetime
from urllib.parse import urljoin

import pytz
import requests
from envparse import env
from iso8601 import parse_date

env.read_envfile()


def parse_links(input):
    for link in input.split(', '):
        found = re.match(r'<([^\>]+)>; rel="(.+)"', link)
        if found:
            link, rel = found.group(1), found.group(2)
            link = link.replace('https://api.github.com/', '')

            yield rel, link


def get(what):
    r = requests.get(urljoin('https://api.github.com/', what), headers={
        'Authorization': 'Token {}'.format(env('GITHUB_TOKEN')),
    })

    return r.json(), dict(parse_links(r.headers['Link']))


def get_events(till: datetime):
    till = till.replace(tzinfo=pytz.timezone('Europe/Moscow'))

    page = '/repos/{}/issues/events'.format(env('GITHUB_REPO'))

    while True:
        got = get(page)
        for event in got[0]:
            if parse_date(event['created_at']) < till:  # stop iteration if we have reached the date after the given
                return

            if(event['event'] == 'closed'):
                yield dict(
                    date=parse_date(event['created_at']),
                    issue_number=event['issue']['number'],
                    issue_title=event['issue']['title'],
                    issue_url=event['issue']['html_url'],
                    assignees=[assignee['login'] for assignee in event['issue']['assignees']],
                    milestone=event['issue']['milestone']['title'] if event['issue']['milestone'] is not None else None,
                )

        page = got[1]['next']
