#!/bin/bash

# Do this first
# ps -ef | grep python | awk '{print $2}' | xargs sudo kill -9 

# and incase of docker daemon error
# sudo systemctl restart docker

sudo nice -n -20 python3 store_docker_stats.py &

noOfDockerProcesses=1
while [ $noOfDockerProcesses -le 7 ]
do
	bash run_mnist.sh config/app"$noOfDockerProcesses"_config.json &
	echo "Docker $noOfDockerProcesses started....."
	noOfDockerProcesses=$(( $noOfDockerProcesses + 1 ))
	sleep 30
done


# docker ps -a
# docker rm <container-id>
# docker ps -a -q | awk '{print $1}' | xargs docker stop
# docker ps -a -q | awk '{print $1}' | xargs docker rm
# ps -ef | grep python | awk '{print $2}' | xargs sudo kill -9