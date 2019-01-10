# daily-hero

Шлет каждый день письмо о том, какие задачи вчера были закрыты
`
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
