import re
from datetime import datetime
from urllib.parse import urljoin

import pytz
import requests
from iso8601 import parse_date


def parse_links(input):
    for link in input.split(', '):
        found = re.match(r'<([^\>]+)>; rel="(.+)"', link)
        if found:
            link, rel = found.group(1), found.group(2)
            link = link.replace('https://api.github.com/', '')

            yield rel, link


def get(what):
    print('get', what)
    r = requests.get(urljoin('https://api.github.com/', what), headers={
        'Authorization': 'Token b09dbe25381718e93a095ec4f6fdb4372cabb41a',
    })

    return r.json(), dict(parse_links(r.headers['Link']))


def get_events(*args, tzinfo=pytz.timezone('Europe/Moscow')):  # noqa: B008
    till = datetime(*args, tzinfo=tzinfo)
    page = '/repos/gdml/a/issues/events'
    while True:
        got = get(page)
        for event in got[0]:
            if parse_date(event['created_at']) < till:
                return

            if(event['event'] == 'closed'):
                yield dict(
                    date=parse_date(event['created_at']),
                    issue=event['issue']['title'],
                    assignees=[assignee['login'] for assignee in event['issue']['assignees']],
                    milestone=event['issue']['milestone']['title'] if event['issue']['milestone'] is not None else None,
                )

        page = got[1]['next']


if __name__ == '__main__':
    print(list(get_events(2019, 1, 10)))
