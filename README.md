# restful_booker_tester

* A service for testing an API playground https://restful-booker.herokuapp.com/
* restful-booker API doc https://restful-booker.herokuapp.com/apidoc/

# Requirements

* Look into pyproject.toml

# Setup

* Install poetry >=2.1.3 https://python-poetry.org/docs/#installing-with-the-official-installer
* Install dependencies for the project: `poetry install --no-root`
* Activate the environment: `poetry shell`

# Run tests
* Run all the tests: `pytest`
* Run a certain class of tests: `pytest -k TestCreateBookingPositive`
* Run a specific test: `pytest -k test_create_booking_with_diff_valid_names`

# Code-style
* flake8, yapf, isort
* Check formatting erorrs: `isort -c -d . ; yapf -dpr .; flake8 .`
* Fix formatting errors: `isort . ; yapf -pir .; flake8 .`
