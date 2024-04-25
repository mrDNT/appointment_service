#!/bin/sh

alembic revision --autogenerate -m 'initial'
alembic upgrade head