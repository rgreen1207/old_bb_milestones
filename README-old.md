# milestones_api

milestones_api is a FastAPI based web application that provides an intuitive and efficient way to manage project milestones. The application is built on the Unicorn web server and utilizes a MariaDB MySQL database for data storage. This ReadMe file serves as a comprehensive guide to help you understand, install, and set up milestones-api, as well as run its unit and integration tests.

## Table of Contents

- [Requirements](#requirements)
- [Local Setup](#local-environment-setup)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Running Unit and Integration Tests](#running-tests)

## Local Environment Setup

See wiki: [pyenv setup](https://github.com/blueboard/milestones-api/wiki/MacOS-Local-Development-Setup)

## Requirements

- Python 3.11 or higher
- Docker Desktop
- pip (Python package manager)


## Installation

1. Clone the repository:
```
git clone https://github.com/blueboard/milestones-api.git
```
2. Navicate to the project root directory:
```
cd ../milestones-api
```

3. (optional) Create a virtual environment

basic format:
```
pyenv virtualenv <python-version> <environemnt name>
```
if `pythin-version` is not specified, the current pyenv global version is used

example command:
```
pyenv virtualenv 3.11.1 myproject
```

4. Install the required dependencies
(optional) be sure that the local environment is activated

```bash
pip install -r requirements.txt
```

5. Create coonfig.py
Get the config file content, create a file in the `src` directory called config.py, and copy the config content into it.


## Database Setup

To set up the database for the milestones-api application, you need to follow these steps:

1. Create a now MariaDB container in Docker

Note: feel free to change `MYSQL_ROOT_PASSWORD`
```
docker run --name my-mariadb -e MYSQL_ROOT_PASSWORD=password -d -p 32776:3306 mariadb:latest
```

2. Use `.sql` config file to create new MySQL database in MariaDB container

Note: local path to the config file must changed. On MacOS, `right-click + option` allows for full file path to be copied
```
docker exec -i my-mariadb sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < /path/to/your/config/file.sql
```

3. (Optional) Log into MariaDB container
```
docker run -it --link my-mariadb:mysql --rm mariadb sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
```

## Running the Application

From root run:
```
python src/app.py
```

## Running Tests

To run the unit and integration tests:
```
pytest
```

or alrernativelty:
```
python -m pytest
```
