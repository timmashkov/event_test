# Event service API

[![python](https://img.shields.io/badge/python-3.12_-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.110.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.29-critical?style=flat-square)](https://www.sqlalchemy.org//)
[![alembic](https://img.shields.io/badge/alembic-1.13.1_-violet?style=flat-square)](https://alembic.sqlalchemy.org//)


## Описание

<details>
<summary><b>ЗАДАНИЕ:</b></summary>

    Технологии:
     - Python
     - FastAPI
     - SQLAlchemy
     - Alembic
     - Uvicorn 
     - Asyncpg

    Реализовано:
      - DDD, CQRS
      - кастомная аутентификация\авторизация с JWT
      - админка
      - миграции на алембик
      - полный асинк
      - 6 сущностей и все слои работы(круд+сервис+ручки)
      - кэширование с помощью Redis

    Эндпоинты:
      - Компания(полный круд + список связанных сотрудников + список связанных курсов + и то и то)
      - Курсы(полный круд + список связанных преподавателей)
      - Сотрудник(полный круд)
      - Юзер(полный круд + логин\логаут\рефреш токена\проверка залогирован или нет + список отзывов)
      - Препод(полный круд)
      - Отзыв(полный круд + список связанных сотрудников + список связанных курсов + и то и то)
 
</details>


## Для запуска проекта

- Cоздать и активировать виртуальное окружение
- Клонировать репозиторий и перейти в него
- python -m pip install --upgrade pip
- pip install -r requirements.txt
- Создать .env по примеру .env_example
- Поднять локально Redis
- Выполнить миграции(alembic upgrade head)
- Запустить проект:

```
cd src
uvicorn runner:start_app --reload
или запустить main.py
```
Запустить сваггер:
```
http://127.0.0.1:8000/docs
```

## Для запуска проекта в докере

- Вписать в .env_prod данные почты
- перейти в директорию проджекта и ввести команду:
```
docker compose up --build
```


### Автор:
Тимур Машков