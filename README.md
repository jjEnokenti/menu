<h1 align="center">RESTful API ресторанного меню</h1>

## Роадмап

- [Стек](#стек)
- [Инструкция по запуск проекта](#инструкция-по-настройке-и-запуску-проекта)
- [Мониторинг](#для-мониторинга-задач)
- [Инструкция по запуску тестов](#инструкция-по-запуску-тестов)
- [Техническое задание](#техническое-задание)
- [Дополнительно](#дополнительно)

## Стек

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10-yellow?&logo=appveyor" alt="">
<img src="https://img.shields.io/badge/PostgreSQL-15.1-orange?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/FastAPI-0.100.0-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Pydantic-2.1.1-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/SQLAlchemy-2.0.19-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Docker-blue?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Docker-compose-blue?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Uvicorn-0.23.0-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/alembic-1.11.1-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Aioredis-2.0.1-red?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/RabbitMQ-3.12-red?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Celery-5.3.1-blue?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Flower-2.0.1-blue?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Google_api_python_client-2.96.0-g?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Openpyxl-3.1.2-g?logo=appveyor" alt="">
</p>

## Инструкция по настройке и запуску проекта

### 1. Склонируйте репозиторий

    git clone https://github.com/jjEnokenti/menu.git

### 2. Настройте окружение

* создайте файл .env по примеру .env.example
* Для работы через Google Sheets **необходимо**
  разместить в корне проекта json файл
  с данными о сервисном аккаунте и назвать его **credentials.json**
  и в env файле укажите id вашей таблицы
* Если нужно администрировать бд через локальный файл, то закомментируйте FILE_READ_MODE в .env

### Запуск проекта без Celery для тестирования Апи через Postman

    make postman-test

### Запуск всего проекта

    make up

### Посмотреть логи API

    make show-logs

### Для остановки контейнеров

    make down

### Все доступные эндоинты можно посмотреть после запуска приложения на странице [docs](http://0.0.0.0:8000/api/v1/docs)


### Для мониторинга задач:

- #### [flower](http://0.0.0.0:5555)
- #### [rabbit](http://0.0.0.0:15672)

## Инструкция по запуску тестов

### 1. Настройте окружение для тестов

#### 1. Дополните .test.env, впишите ваши имя пользователя бд, пароль и имя базы

### Команда для сборки контейнеров с тестами и их запуска

    make start-test

### Команда для просмотра результата тестов

    make show-result

### Для остановки тестовых контейнеров

    make drop-test

## Техническое задание

<details>
<summary>1 Часть</summary>
<h4>
Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции. Для проверки задания, к презентаций будет приложена Postman коллекция с тестами. Задание выполнено, если все тесты проходят успешно.

Даны 3 сущности:

- Меню
- Подменю
- Блюдо

</h4>
<p>

Зависимости:

- У меню есть подменю, которые к ней привязаны.
- У подменю есть блюда.

Условия:

- Блюдо не может быть привязано напрямую к меню, минуя подменю.
- Блюдо не может находиться в 2-х подменю одновременно.
- Подменю не может находиться в 2-х меню одновременно.
- Если удалить меню, должны удалиться все подменю и блюда этого меню.
- Если удалить подменю, должны удалиться все блюда этого подменю.
- Цены блюд выводить с округлением до 2 знаков после запятой.
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
- Во время запуска тестового сценария БД должна быть пуста.

</p>
</details>

<details>
<summary>2 Часть</summary>
<h4>
В этом домашнем задании надо написать тесты для ранее разработанных ендпоинтов вашего API после Вебинара №1.
</h4>

<p>
Обернуть программные компоненты в контейнеры.

Контейнеры должны запускаться по одной команде “docker-compose up -d” или той которая описана вами в readme.md.

Образы для Docker:

- (API) python:3.10-slim
- (DB) postgres:15.1-alpine

1. Написать CRUD тесты для ранее разработанного API с помощью библиотеки pytest
2. Подготовить отдельный контейнер для запуска тестов. Команду для запуска указать в README.md
3. `*` Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
4. `**` Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest

*Если FastAPI синхронное - тесты синхронные, Если асинхронное - тесты асинхронные<br>
**Оборачиваем приложение в докер.<br>
***CRUD – create/update/retrieve/delete.
</p>
</details>

<details>
<summary>3 Часть</summary>
<p>

1. Вынести бизнес логику и запросы в БД в отдельные слои приложения.
2. Добавить кэширование запросов к API с использованием Redis. Не забыть про инвалидацию кэша.
3. Добавить pre-commit хуки в проект. Файл yaml будет прикреплен к ДЗ.
4. Покрыть проект type hints (тайпхинтами)
5. `*` Описать ручки API в соответствий c OpenAPI
6. `**` Реализовать в тестах аналог Django reverse() для FastAPI

Требования:

- Код должен проходить все линтеры.
- Код должен соответствовать принципам SOLID, DRY, KISS.
- Проект должен запускаться по одной команде (докер).
- Проект должен проходить все Postman тесты (коллекция с Вебинара №1).
  -Тесты написанные вами после Вебинара №2, должны быть актуальны, запускать и успешно проходить

Дополнительно:<br>
Контейнеры с проектом и с тестами запускаются разными командами.

</p>
</details>

<details>
<summary>4 Часть</summary>

<p>

В этом домашнем задании необходимо:

1. Переписать текущее FastAPI приложение на асинхронное выполнение
2. Добавить в проект фоновую задачу с помощью Celery + RabbitMQ.
3. Добавить эндпоинт (GET) для вывода всех меню со всеми связанными подменю и со всеми связанными блюдами.
4. Реализовать инвалидация кэша в background task (встроено в FastAPI)
5. `*` Обновление меню из google sheets раз в 15 сек.
6. `**` Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx

<b>Фоновая задача</b>:
* синхронизация Excel документа и БД.
* В проекте создаем папку admin. В эту папку кладем файл Menu.xlsx (будет прикреплен к ДЗ). Не забываем запушить в гит.
* При внесении изменений в файл все изменения должны отображаться в БД. Периодичность обновления 15 сек. Удалять БД при каждом обновлении – нельзя.

Требования:

- Данные меню, подменю, блюд для нового эндпоинта должны доставаться одним ORM-запросом в БД (использовать подзапросы и агрегирующие функций SQL).
- Проект должен запускаться одной командой
- Проект должен соответствовать требованиям всех предыдущих вебинаров. (Не забыть добавить тесты для нового API эндпоинта)

</p>
</details>

## Дополнительно

<h3>
<details>
<summary>Задания со звездочками</summary>

1. Задания из 2 части:

- `*` Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.<br>
<b>src/api/repositories/menu.py</b> - Функция get_statement возвращает такой запрос для меню
<b>src/api/repositories/submenu.py</b> - Функция get_statement возвращает такой запрос для подменю


- `**` Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest <br>
В файле tests/dynamic_data_test.py реализован данный тест скрипт.

2. Задания из 3 части:

- `*` Описать ручки API в соответствий c OpenAPI <br>
Реализованно, можно посмотреть документацию по [ссылке](http://0.0.0.0/api/v1/docs)
после запуска проекта.

- `**` Реализовать в тестах аналог Django reverse() для FastAPI <br>
В фикстурах к тестам реализованно посредством дополнения функции Fastapi url_path_for

3. Задания из 4 части:

- `*` Обновление меню из google sheets раз в 15 сек.

в папке src/celery в файле google_cloud_connect описано подключение и получение данных из Гугл таблицы

</details>
</h3>

[В начало](#роадмап)
