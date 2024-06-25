# TODO API

This is a small repo I'm using to test some react work.

## Setup

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Create the database:

```
createdb todo-api
```

Replace the `.env.example` with your own `.env`. Use the database name of `todo-api`.

Setup database:

```
alembic upgrade head
```

Run the API:

```
uvicorn main:app --reload
```

The API should be up and running at this point.
