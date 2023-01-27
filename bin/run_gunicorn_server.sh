#!/bin/bash

# Get AbPath
PROJECT_PATH=$(dirname $(dirname $(realpath $0)))
SETTING_FILE=system/environments.yaml  # environments 파일 경로 매칭 필요

# include parse_yaml function
. $PROJECT_PATH/bin/yaml_reader.sh

# read yaml file
eval $(parse_yaml $PROJECT_PATH/$SETTING_FILE "")

# run uwsgi server
# Gunicorn Guide: https://docs.gunicorn.org/en/latest/index.html
gunicorn \
    --name $server_name \
    --bind $server_host:$server_port \
    --env DJANGO_SETTINGS_MODULE=$server_name.settings \
    --env PYTHONENCODING=UTF-8 \
    --workers $server_processes \
    --log-level debug \
    --access-logfile $PROJECT_PATH/$settings_log_dir/gunicorn_access.log \
    --error-logfile $PROJECT_PATH/$settings_log_dir/gunicorn_error.log \
    $server_name.wsgi:application
