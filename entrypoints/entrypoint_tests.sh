#!/bin/bash

echo 'RUN TEST'

chmod +x .pytest_cache/
pytest -s
