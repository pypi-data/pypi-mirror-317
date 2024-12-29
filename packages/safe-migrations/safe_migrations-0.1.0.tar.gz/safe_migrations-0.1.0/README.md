# Safe Migrations

A Django package to safely generate and apply migrations from historical commits.

## Installation

Install the package via pip:

```bash
pip install safe-migrations
```

## Usage

```bash
python manage.py safe_migration [commit_hash]
```

## Features

Automatically identifies model changes across commits.
Generates and applies all missing migrations safely.
