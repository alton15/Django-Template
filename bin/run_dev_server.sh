#!/bin/bash

# Get AbPath
PROJECT_PATH=$(dirname $(cd $(dirname $0) && pwd -P))
SETTING_FILE=system/environments.yaml  # environments 파일 경로 매칭 필요

# include parse_yaml function
. $PROJECT_PATH/bin/yaml_reader.sh

# read yaml file
eval $(parse_yaml $PROJECT_PATH/$SETTING_FILE "")

# source activate backend-test  # 가상환경 이름 지정 필요

# If need GPU Use.
# CUDA_VISIBLE_DEVICES=2 python manage.py runserver $server_host:$server_port

python manage.py runserver $server_host:$server_port
