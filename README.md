

<h1 align="center">API ресторанного меню</h1>

---

<h3 align="center">Стек</h3>
<p align="center">
<img src="https://img.shields.io/badge/Python-3.10-yellow?&logo=appveyor" alt="">
<img src="https://img.shields.io/badge/PostgreSQL-15.1-orange?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/FastAPI-0.100.0-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/SQLAlchemy-2.0.19-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Docker-blue?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Docker-compose-blue?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Uvicorn-0.23.0-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/alembic-1.11.1-green?logo=appveyor" alt="">
<img src="https://img.shields.io/badge/Aioredis-2.0.1-red?logo=appveyor" alt="">
</p>

---

<h3 align="center">Все доступные эндоинты можно посмотреть после запуска приложения
на странице <a href="http://0.0.0.0:8000/api/v1/docs/">docs</a>.</h3>

    0.0.0.0:8000/api/v1/docs/

---

<h3 align="center">Инструкция по установке и запуску проекта</h3>

### 1. Склонируйте репозиторий
    git clone https://github.com/jjEnokenti/menu.git

### 2. Настройте окружение
#### 1. создайте файл .env по примеру .env.example

### 3. Можете запускать приложение
    make up
### 4. Посмотреть логи
    make show-logs
### 5. Для остановки контейнеров
    make down

---

<h3 align="center">Инструкция по запуску тестов</h3>

### 1. Настройте окружение для тестов
#### 1. Дополните .test.env, впишите ваши имя пользователя бд, пароль и имя базы

### 1. Команда для сборки контейнеров с тестами и их запуска
    make start-test
### 2. Команда для просмотра результата тестов
    make show-result
### 3. Для остановки тестовых контейнеров
    make drop-test

---
