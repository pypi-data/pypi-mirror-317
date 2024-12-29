# pydantic-extra

Данный модуль содержит готовые модели pydantic для частых задач.

установка
`pip install pydantic-extra`

# pydantic-extra.smtp

## модель MailServer

* `smtp_host` - хост
* `smtp_port` - порт (по умолчанию: 465)
* `smtp_ssl` - использовать ssl (по умолчанию: True)
* `smtp_login`/`smtp_password` - данные для авторизации
* `from_addr` - имя отправителя (по умолчанию: `smtp_login`)

# pydantic-extra.db

Требует дополнительные зависимости `db` (sqlalchemy) \
`pip install pydantic-extra[db]`

## модели DB(базовая модель), SQLite, Mysql(в т.ч. для MariaDB), AnyDB

### SQLite

* `type` - `sqlite`
* `path` - путь до БД

### AnyDB

* `type` - `any`
* `str` - строка подключения для sqlalchemy

### Mysql

* `type` - `mysql` или `mariadb`
* `host` - хост
* `port` - порт (по умолчанию: 3306)
* `login`/`password` - данные для авторизации
* `encoding` - кодировка (по умолчанию: `utf8mb4`)
* `database` - имя БД

### DB

* `connect_str()` - возвращает строку подключения для sqlalchemy или sqlalchemy.URL
* `setup()` - настраивает sqlalchemy для работы с данным диалектом

## использование

```python
from pydantic import BaseModel, Field
from pydantic_extra.db import T_DB


class ExampleConfig(BaseModel):
    db: T_DB = Field(discriminator='type')
```

С базой данной SQLite по умолчанию

```python
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_extra.db import T_DB, SQLite


class ExampleConfig(BaseModel):
    db: T_DB = Field(SQLite(type="sqlite", path=Path('example.sqlite')), discriminator='type')
```
