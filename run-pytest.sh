#!/usr/bin/env bash

# # build the docker image
# docker build -f ./Docker/Dockerfile.milestones_api_localhost  -t milestones_api-milestones_api .

# # run the tests in a docker container
# docker run --env-file .env --name milestones_api_test milestones_api-milestones_api

# # get the test results
# docker logs milestones_api_test > test_results.log

# # remove the docker container
# docker rm milestones_api_test

#!/usr/bin/env bash

# start containers in background
docker-compose up --build --detach


# run tests
# if nor argument, run all tests, if an argument, then just run the given file
# if [ -z "$1" ]; then
#    docker exec -i milestones_api pytest -v
# else
#    docker exec -i milestones_api pytest -v /app/tests/$1
# fi

TEST_DIR=${1:-/app/tests}

docker exec -i milestones_api pytest -v ${TEST_DIR}



status=$?
if [ $status -ne 0 ]; then
    echo "*****************************************"
    echo "* Houston, there were test failures :-< *"
    echo "*****************************************"
else
    echo "*****************************************"
    echo "*       All tests passed!  Huzzah!      *"
    echo "*****************************************"
fi

# cleanup
docker compose down
