# daily-hero

Шлет каждый день письмо о том, какие задачи вчера были закрыты:

![43f59d0b-088d-5bea-eacc-0a66bd7f2505](https://user-images.githubusercontent.com/1592663/58763095-92099680-855f-11e9-8812-f5cb419a7ab8.png)

## Installation

```yaml
version: '3.6'

services:
  daily-hero:
    image: gdml/daily-hero:0.0.1
    environment:
      GITHUB_REPO: gdml/a
      GITHUB_TOKEN: TOKEN
      TO: developers@gdml.ru
      FROM: GitHub <developers@gdematerial.ru>
      MAILGUN_API_KEY: KEY
      MAILGUN_DOMAIN: ***REMOVED***
```

## Contributing
Запилите новый релиз, дождитесь билда и обновите образ на проде
