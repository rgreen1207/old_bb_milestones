#!/usr/bin/env bash

# MariaDB [(none)]> SELECT @@character_set_database;
# +--------------------------+
# | @@character_set_database |
# +--------------------------+
# | utf8mb4                  |
# +--------------------------+

# this is a hack https://stackoverflow.com/questions/1916392/how-can-i-get-rid-of-these-comments-in-a-mysql-dump
mysqldump -uroot -ppassword \
    --no-data  \
    blueboard_milestones > schema.sql # | grep -v '^\/\*![0-9]\{5\}.*\/;$' > schema.sql