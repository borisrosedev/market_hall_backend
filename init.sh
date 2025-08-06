#!/bin/bash
set -e 
CYAN_COLOR='\033[1;36m'
GREEN_COLOR='\033[1;34m'
NO_COLOR='\033[0m'


function git_init {

    if [[ -e ".git" ]]; then 
        echo -e "${CYAN_COLOR}this is already a local git repository${NO_COLOR}"
    else
        git init 
        echo ".venv" >> .gitignore 
    fi
}


function activate_venv {
    echo -e "${CYAN_COLOR}Would you like to activate the virtual environment ? ${NO_COLOR}"
    read -r execute_answer

    if [ "$execute_answer" = 'yes' ]; then  
        source .venv/bin/activate
        echo -e "${GREEN_COLOR}🚀 virtual environment activated ${NO_COLOR}"
    else
        exit 1
    fi
}

function python_env {  
    if [[ -e ".venv" ]]; then 
        echo -e "${CYAN_COLOR}There is already .venv in this app ${NO_COLOR}"
    else
       echo -e "${GREEN_COLOR}Adding the module venv to the app${NO_COLOR}"
       python3 -m venv .venv
       
    fi
    activate_venv
}

git_init
python_env

