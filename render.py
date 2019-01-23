import pystache

TEMPLATE = r"""
{{#heroes}}
    {{name}}:
    {{#issues}}
        — {{ title }} ({{ url }})
    {{/issues}}

{{/heroes}}

Ваш гитхаб
"""


def render_text(ctx):
    return pystache.render(TEMPLATE, ctx)


def render_header(hero):
    return '<h3>{}</h3>'.format(hero)


def render_link(url, text):
    return '<a href="{}">{}</a>'.format(url, text)


def render_item(item):
    link = render_link(item['url'], item['number'])
    return '<li>{} ({})</li>'.format(item['title'], link)


def render_list(issues):
    items = ''.join([render_item(issue) for issue in issues])
    return '<ul>{}</ul>'.format(items)


def rende_hero(hero):
    header = render_header(hero['name'])
    issues = render_list(hero['issues'])
    section = ''.join([header, issues])
    return '<section>{}</section></br></br>'.format(section)


def render_body(heroes):
    return ''.join([rende_hero(hero) for hero in heroes])


def render_footer(text='Ваш гитхаб'):
    return '<p>{}</p>'.format(text)


def render_html(ctx):
    body = render_body(ctx['heroes'])
    footer = render_footer()
    return ''.join([body, footer])
