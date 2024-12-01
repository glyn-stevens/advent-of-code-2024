$TARGER_DIR=("advent_of_code")

"`nRunning ruff format:"
poetry run ruff format $TARGER_DIR

"`nRunning ruff lint:"
poetry run ruff check $TARGER_DIR

"`nRunning mypy:"
poetry run mypy $TARGER_DIR --ignore-missing-imports --check-untyped-defs