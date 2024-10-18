format:
  uv run ruff format
  
check: format
  uv run ruff check --fix

test *params:
  uv run pytest {{params}}

nox *params:
  uv run nox -db uv {{params}}

checkall: (nox "-k" "check")

testall: (nox "-k" "test")
