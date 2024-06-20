![repo size](https://img.shields.io/github/repo-size/foxygen-d/cat_charity_fund)
![py version](https://img.shields.io/pypi/pyversions/3)
-----
[![Python](https://img.shields.io/badge/Python-3.9|3.10|3.11-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![pydantic](https://img.shields.io/badge/pydantic-2.6.3-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/pydantic/2.6.3/)

[![fastapi](https://img.shields.io/badge/fastapi-0.110.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/fastapi/0.110.0/)
[![fastapi limiter](https://img.shields.io/badge/fastapi_limiter-0.1.6-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/fastapi_limiter/0.1.6/)
[![uvicorn](https://img.shields.io/badge/uvicorn-0.28.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/uvicorn/0.28.0/)
[![gunicorn](https://img.shields.io/badge/gunicorn-21.2.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/gunicorn/21.2.0/)
[![redis](https://img.shields.io/badge/redis-5.0.3-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/redis/5.0.3)

Сервис мемов

[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.29-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/sqlalchemy/2.0.29/)
[![alembic](https://img.shields.io/badge/alembic-1.13.1-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/alembic/1.13.1/)
[![asyncpg](https://img.shields.io/badge/asyncpg-0.29.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/asyncpg/0.29.0/)
[![httpx](https://img.shields.io/badge/httpx-0.29.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/httpx/0.27.0/)

Сервис сохрание файлов в S3 хранилище

[![aiobotocore](https://img.shields.io/badge/aiobotocore-21.2.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/aiobotocore/2.13.0/)

---
[![Poetry](https://img.shields.io/badge/Poetry-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/poetry/)
[![Ruff](https://img.shields.io/badge/Ruff-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/ruff/)
[![mypy](https://img.shields.io/badge/mypy-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/mypy/)


# Test-case-MadSoft

Тестовое задание для компании MadSoft

## Описание

Веб-приложение на Python, которое предоставляет API для работы с коллекцией мемов. Приложение состоит из двух сервисов: сервис с публичным API с бизнес-логикой и сервис для работы с медиа-файлами, используя S3-совместимое хранилище.  

Функциональность:

●  GET /memes: Получить список всех мемов (с пагинацией).

●  GET /memes/{id}: Получить конкретный мем по его ID.

●  POST /memes: Добавить новый мем (с картинкой и текстом).

●  PUT /memes/{id}: Обновить существующий мем.                                        

●  DELETE /memes/{id}: Удалить мем. 

Требования:                          

●  Используется реляционная СУБД для хранения данных.

●  Обеспечивается обработка ошибок и валидация входных данных.

●  Используется Swagger/OpenAPI для документирования API. По умолчанию документация api доступна по пути - /api/openapi

●  Создан docker-compose.yml для запуска проекта.


## Инструкция по развёртыванию проекта

* клонировать проект на компьютер
    ```bash
    git clone git@github.com:MultikPatin/Test-case-MadSoft.git
    ```
* Установить менеджер зависимостей poetry
    ```bash
    python -m pip install poetry
    ```
  
Проект состоит из 2 сервисов, каждый со своим независимым друг от друга окружением.
Сервисы расположены в папках:
  - mems_api
  - s3_saver

Перейдите в нужный сервис и установите зависимости.

* запуск виртуального окружения
    ```bash
    poetry shell
    ```
* установить зависимости
    ```bash
    poetry install --all-extras --with dev
    ```
Сервис реализован в контейнерах Docker.
Для запуска полного проекта выполните следующую команду в корневом каталоге.

* запуск docker-compose
    ```bash
    docker-compose up -d -f docker-compose.yml
    ```
