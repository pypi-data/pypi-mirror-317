# django-pgcli5

[![Build Status](https://github.com/offbyone/django-pgcli/actions/workflows/ci.yml/badge.svg)](https://github.com/offbyone/django-pgcli/actions/workflows/ci.yml)

[![PyPI version](https://badge.fury.io/py/django-pgcli5.svg)](https://badge.fury.io/py/django-pgcli5) 

![PyPI - License](https://img.shields.io/pypi/l/django-pgcli5)

Replaces your existing *psql* cli for Postgres with *pgcli* which provides enhancements such as auto-completion and syntax highlighting. Visit the [pgcli website](https://www.pgcli.com/) to learn more about the **pgcli** client.

## Installation

To install the package:

    `pip install django-pgcli5`

Add `django_pgcli5` to your `INSTALLED_APPS` setting in your settings.py file.

    INSTALLED_APPS = [
        ...,
        'django_pgcli5',
    ]

## Usage

To use the `pgcli` command with your project, call the `dbshell` command.

    ./manage.py dbshell
