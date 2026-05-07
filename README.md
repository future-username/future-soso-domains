# 🛡️ future-soso-domains

Списки **IP-адресов и доменов** для блокировки от злых духов 👻 — телеметрии, трекеров, рекламной нечисти и прочих сущностей, которым не место в твоей сети.

Подготовлено для использования в [Podkop](https://github.com/itdoginfo/podkop) на роутерах с OpenWrt в режиме **Block**.

## 📂 Содержимое

| Файл | Что внутри | Формат |
|------|------------|--------|
| `domains.json` | Доменные имена для блокировки на DNS-уровне | sing-box rule-set (JSON) |
| `facetime-ip.json` | IP-адреса и подсети | plain text, по одному значению в строке |

## 🚀 Подключение к Podkop

В веб-интерфейсе LuCI:

1. Открой **Podkop → правило / instance**
2. Выбери режим **Block**
3. Включи **«Удалённый список доменов»** — вставь raw-ссылку на `domains.json`
4. Включи **«Удалённый список подсетей»** — вставь raw-ссылку на `facetime-ip`
5. Сохрани и применить
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

Списки пополняются по мере появления новых злых духов в эфире. Чтобы быть в курсе — нажми **Watch → Custom → Releases** на странице репозитория.

## ⚠️ Дисклеймер

Списки собраны на основе личного опыта и открытых источников. Используй на свой страх и риск: никаких гарантий, что под раздачу случайно не попадёт что-то полезное. Если что-то сломалось или хочется добавить новую сущность в список — открывай issue или присылай PR.

## 📜 Лицензия

MIT
