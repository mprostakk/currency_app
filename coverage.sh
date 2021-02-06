#!/bin/bash

coverage run --branch --source=currency_app,subscription,users ./manage.py test
coverage report
coverage html -d coverage-report
