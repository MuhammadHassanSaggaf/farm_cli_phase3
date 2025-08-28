# Farm CLI (Phase 3 Project)

Simple menu-driven command-line application to manage animals and feed on a farm. Built with Python and SQLAlchemy (ORM).

## Features
- Menu-based CLI with loops and input validation.
- SQLAlchemy models with class methods for create/delete/get_all/find_by_id.
- One-to-many relationship: `Animal` -> `AnimalFeed` events (feed history).
- Property methods that validate attributes on assignment.
- Uses Pipenv for virtual environment and dependencies.

## Quickstart
1. Install Pipenv if you don't have it: `pip install pipenv`.
2. From project root run:
   ```bash
   pipenv install
   pipenv shell
   python run.py
