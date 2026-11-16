# 🛡️ future-soso-domains

Списки **IP-адресов и доменов** для блокировки от злых духов 👻 — телеметрии, трекеров, рекламной нечисти и прочих сущностей, которым не место в твоей сети.

Подготовлено для использования в [Podkop](https://github.com/itdoginfo/podkop) на роутерах с OpenWrt в режиме **Block**.

## 📂 Содержимое

| Файл | Что внутри | Формат |
|------|------------|--------|
| `domains.json` | Доменные имена для блокировки на DNS-уровне | sing-box rule-set (JSON) |
| `facetime-ip.json` | IP-подсети с ограничениями UDP и портов | sing-box rule-set (JSON) |

## 🚀 Подключение к Podkop

В веб-интерфейсе LuCI:

1. Открой **Podkop → правило / instance**
2. Выбери режим **Block**
3. Включи **«Удалённый список доменов»** — вставь raw-ссылку на `domains.json`
4. Для `facetime-ip.json` используй подключение, которое поддерживает sing-box JSON rule-set: файл содержит условия UDP и портов, поэтому его нельзя загружать как обычный текстовый список подсетей.
5. Сохрани и примени
6. Готово — злые духи изгнаны 🧹✨

Podkop сам подтянет списки и будет периодически обновлять их по расписанию (по умолчанию — раз в сутки).

## 🔗 Raw-ссылки для вставки

**Домены:**

```
https://raw.githubusercontent.com/future-username/future-soso-domains/main/domains.json
```

**IP и подсети:**

```
https://raw.githubusercontent.com/future-username/future-soso-domains/main/facetime-ip.json
```

Альтернативный формат (через `refs/heads/`, иногда стабильнее с кешированием GitHub):

```
https://raw.githubusercontent.com/future-username/future-soso-domains/refs/heads/main/domains.json
https://raw.githubusercontent.com/future-username/future-soso-domains/refs/heads/main/facetime-ip.json
```

## 🔄 Обновление

GitHub Actions автоматически пересобирает `domains.json` и `facetime-ip.json` ежедневно в **06:23 по Москве (03:23 UTC)**. Запуск может задержаться на стороне GitHub. Изменения сохраняются коммитом только тогда, когда содержимое списков изменилось.

Источники обновлений:

- Домены GitHub (включая Copilot и npm), JetBrains, Notion, PlayStation, Ubisoft и RuTracker — соответствующие списки [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community/tree/master/data). Точные домены `full:` сохраняются как `domain`, остальные — как `domain_suffix`.
- Подсети Telegram — [официальный список IPv4 и IPv6](https://core.telegram.org/resources/cidr.txt). Они обновляются только в третьем правиле `facetime-ip.json`; условие UDP сохраняется.
- Остальные домены, подсети FaceTime и правила удалённого доступа остаются ручными: автоматического источника для них пока нет. DNS-адреса доменов не добавляются в подсети, чтобы не затрагивать общие IP CDN.

Для ручных дополнений редактируй `sources/manual/domains.json` и `sources/manual/facetime-ip.json`. Исходные записи перенесены туда; Telegram-подсети в третьем правиле заполняет сборщик. Список обновляемых сервисов находится в `sources/config.json`. Файлы в корне пересоздаются автоматически, поэтому ручные изменения нужно вносить в `sources/manual/`.

Ручной запуск: **Actions → Update domains and IP ranges → Run workflow**. Проверки выполняются перед обновлением; если источник недоступен, пуст или содержит ошибку, новые списки не публикуются. Секреты и отдельный токен не нужны: используется `GITHUB_TOKEN` с правом `contents: write`.

Локальная проверка (Python 3.12):

```sh
python -m unittest discover -s tests -v
python scripts/update_lists.py
```

В публичном репозитории GitHub может отключить запуск по расписанию после 60 дней без активности. Если это произойдёт, включи workflow снова во вкладке Actions.

## ⚠️ Дисклеймер

Списки собраны на основе личного опыта и открытых источников. Используй на свой страх и риск: никаких гарантий, что под раздачу случайно не попадёт что-то полезное. Если что-то сломалось или хочется добавить новую сущность в список — открывай issue или присылай PR.

## 📜 Лицензия

MIT
