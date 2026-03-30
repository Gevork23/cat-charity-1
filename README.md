# QRKot

Сервис для Благотворительного фонда поддержки котиков.

## Описание

Проект позволяет:
- создавать благотворительные проекты;
- принимать пожертвования;
- автоматически распределять пожертвования по открытым проектам по принципу FIFO:
  сначала закрываются самые старые открытые проекты.

## Стек

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- SQLite

## Как запустить проект

Клонировать репозиторий и перейти в него:

```bash
git clone https://github.com/Gevork23/cat-charity-1.git
cd cat-charity-1
```
Создать и активировать виртуальное окружение:
```bash
py -3.12 -m venv venv
source venv/Scripts/activate
```
Установить зависимости:
```bash
pip install -r requirements.txt
```
Применить миграции:
```bash
alembic upgrade head
```
Запустить проект:
```bash
uvicorn app.main:app --reload
```
Документация API

После запуска документация доступна по адресу:

Swagger UI: http://127.0.0.1:8000/docs
Основные эндпоинты
Проекты
```
GET /charity_project/ — получить список проектов
POST /charity_project/ — создать проект
PATCH /charity_project/{project_id} — отредактировать проект
DELETE /charity_project/{project_id} — удалить проект
```
Пожертвования
```
GET /donation/ — получить список пожертвований
POST /donation/ — создать пожертвование
```