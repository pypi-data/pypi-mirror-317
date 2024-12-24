#!/bin/sh
set -e

cd /run

if test -z "${LOGGING_CONFIG_FILE}" ; then
    uv run lemmy2fedi /config/config.toml
else
    uv run lemmy2fedi /config/config.toml --logging-config=${LOGGING_CONFIG_FILE}
fi
