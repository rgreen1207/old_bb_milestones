#!/usr/bin/env bash
#
# This is the Docker entrypoint script for running the Milestones app in a hosted environment
#
echo "Cleaning up Python..."
find /app -name "*.pyc" -exec rm -f {} \;

echo "Sleeping for 10 seconds to allow Maria DB to start..."
sleep 10;

cat << EOF >> /etc/bash.bashrc
alias ls='ls -la'
alias bb-mysql="mysql -v -u$MYSQL_USER -p${MYSQL_PASSWORD} -h${MYSQL_HOSTNAME} ${MYSQL_DATABASE}"
alias bb-clean-db="bb-mysql < migrations/milestones_nodata_v1.9.3.sql"
EOF

if [ -f "${ALEMBIC_INI_FILE}" ]; then
    echo "Alembic config file '${ALEMBIC_INI_FILE}' exists, getting Alembic ready..."
    export CONN="sqlalchemy.url = mysql+pymysql\:\/\/${MYSQL_USER}\:${MYSQL_PASSWORD}\@${MYSQL_HOSTNAME}\:${MYSQL_PORT}\/${MYSQL_DATABASE}"

    # back up original ini file for good measure
    cp ${ALEMBIC_INI_FILE} "${ALEMBIC_INI_FILE}.bak"
    echo "Setting alembic connection string to use env vars for sqlalchemy.url..."

    # replace the connection string with the new connection string
    sed -i "s/sqlalchemy.url.*/$CONN/" ${ALEMBIC_INI_FILE}

    echo "Running alembic migrations..."
    alembic upgrade head
else
    echo "Alembic config file '${ALEMBIC_INI_FILE}' is not set or does not exist, skipping Alembic migrations..."
fi

# Append our cron to the system crontab and start crond
if [ ! -z ${CRON} ]; then
    echo "Configuring cron..."
    # envsubst is used here to put a bearer token into the crontab
    envsubst < /crontab >> /etc/crontab
    crontab /etc/crontab
    service cron start
    service cron status
else
    echo "Skipping cron..."
fi

# TODO decide if we want to use Datadog, e.g.
# ddtrace-run uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80 --use-colors
uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80 --use-colors
