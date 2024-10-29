#!/usr/bin/env bash

docker node inspect <id-node> --format "{{ .ManagerStatus.Leader }}"


# get the IDs of anyone that's 
MANAGERS=( $(docker node ls --filter "role=manager" --quiet) )
for i in "${MANAGERS[@]}"
do
   # echo "Manager is $i"
   # 
   # Address:		172.27.0.4
   # Address:		172.27.0.4:2377
   docker node inspect $i --pretty | grep Address | grep -v 2377 | awk '{print $2}'
done