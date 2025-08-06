#!/bin/bash
set -e
#CYAN_COLOR='\033[1;36m'
GREEN_COLOR='\033[1;34m'
NO_COLOR='\033[0m'

export FLASK_APP=app:create_app
export FLASK_DEBUG=1
echo -e "${GREEN_COLOR}🚀 Executing run_flask.sh ${NO_COLOR}"
flask run

