#!/bin/bash

# Get AbPath
PROJECT_PATH=$(dirname $(dirname $(realpath $0)))
SETTING_FILE=system/environments.yaml  # environments 파일 경로 매칭 필요

# include parse_yaml function
. $PROJECT_PATH/bin/yaml_reader.sh

# read yaml file
eval $(parse_yaml $PROJECT_PATH/$SETTING_FILE "")

# run uwsgi server
# Django Guide: https://docs.djangoproject.com/ko/3.2/howto/deployment/wsgi/uwsgi/
uwsgi --chdir=$PROJECT_PATH \
    --module=$server_name.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=$server_name.settings \
    --env PYTHONENCODING=UTF-8 \
    --master \
    --pidfile=/tmp/project-master.pid \
    --$server_protocol=$server_host:$server_port \
    --processes=$server_processes \
    --uid=root \
    --gid=root \
    --harakiri=$server_harakiri \
    --max-requests=$server_maxrequests \
    --log-maxsize=$server_maxlogs \
    --vacuum \
    --logger file:$PROJECT_PATH/$settings_log_dir/uwsgi.log
