#!/bin/bash
set -e

echo 'RUN TEST'

chmod +x ./.pytest_cache/

pytest -s
