#!/bin/bash
# typeset -A config

# while IFS== read -r key value; do
#     config["$key"]="$value"
# done < <(jq -r '.SITE_DATA | to_entries | .[] | .key + "=" + .value ' /home/abhijay/CS_533_Project/config/app1_config.json)

# echo "'$config[docker_name]'"

dockerName=`cat $1 | jq '.docker_name'`
modelName=`cat $1 | jq '.model_name'`

redis-cli SET `echo $dockerName | xargs` `echo $modelName | xargs`

start=`date +%s`
docker run --name `echo $dockerName | xargs` --rm -it -v /home/abhijay/CS_533_Project:/workspace pytorch/pytorch python main.py --configFileName $1
# docker run --name `echo $dockerName | xargs` --rm -it -v /home/abhijay/CS_533_Project:/workspace custom_pytorch_docker python main.py --configFileName $1
end=`date +%s`
runtime=$((end-start))
echo $runtime

redis-cli GET `echo $dockerName | xargs`

redis-cli DEL `echo $dockerName | xargs`