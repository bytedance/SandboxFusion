#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"/..

HOST=${HOST:-127.0.0.1}
make run HOST="${HOST}" PORT=${_BYTEFAAS_RUNTIME_PORT:-8080}
