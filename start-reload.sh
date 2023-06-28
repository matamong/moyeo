#! /usr/bin/env sh
set -e

echo  "-------------Strat Reload .sh starting...."

if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
    echo "------Module Name = app.main"
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
    echo "------Module Name = main""
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-src/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "-------------Running script $PRE_START_PATH"
    # shellcheck source=-/app/prestart.sh
    . "$PRE_START_PATH"
    echo "-------------Prestart Done."
else
    echo "------------There is no script $PRE_START_PATH"
fi

# Start Uvicorn with live reload
exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
