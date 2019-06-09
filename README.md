# Ежедневный герой

Шлет каждый день письмо о том, какие задачи вчера были закрыты:

![43f59d0b-088d-5bea-eacc-0a66bd7f2505](https://user-images.githubusercontent.com/1592663/58763095-92099680-855f-11e9-8812-f5cb419a7ab8.png)

## Installation

Для работы сервиса нужен докер и бесплатный аккаунт на Mailgun.

```yaml
version: '3.6'

services:
  daily-hero:
    image: gdml/daily-hero:1.0.4
    environment:
      GITHUB_REPO: <Your repo path, like gdml/a>
      GITHUB_TOKEN: <Your token, get it at https://github.com/settings/tokens>
      TO: developers@gdml.ru
      FROM: GitHub <developers@gdematerial.ru>
      MAILGUN_API_KEY: KEY
      MAILGUN_DOMAIN: em.gdematerial.ru
```

## Contributing
Сборка образов на докерхабе происходит автоматически из релизов.

Чтобы обновить прод — поменяйте руками версию образа.
