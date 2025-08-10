#!/bin/bash
set -e 
CYAN_COLOR='\033[1;36m'
GREEN_COLOR='\033[1;34m'
NO_COLOR='\033[0m'

function getOs() { 

unameOut=$(uname -a)
OS_NAME="UNKNOWN"
case "${unameOut}" in
    *Microsoft*)     OS="WSL";; #must be first since Windows subsystem for linux will have Linux in the name too
    *microsoft*)     OS="WSL2";; #WARNING: My v2 uses ubuntu 20.4 at the moment slightly different name may not always work
    Linux*)     OS="Linux";;
    Darwin*)    OS="Mac";;
    CYGWIN*)    OS="Cygwin";;
    MINGW*)     OS="Windows";;
    *Msys)     OS="Windows";;
    *)          OS="UNKNOWN:${unameOut}"
esac 
if [[ ${OS} == "Windows" || ${OS} == "Cygwin" || ${OS} == "MINGW" || ${OS} == "Msys" ]]; then
  
  OS_NAME="WIN"
elif [[  ${OS} == "Mac" ]]; then
    OS_NAME="MAC"
 else 
    OS_NAME="UNK" 
fi
}
 

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
        if [[ ${OS_NAME} == "WIN" ]]; then  
            source .venv/Scripts/activate
        else 
            source .venv/bin/activate
        fi
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
getOs
echo -e "${CYAN_COLOR}$Detected  os ${OS_NAME} ${NO_COLOR}"

git_init
python_env

 
if [[ ${OS_NAME} == "WIN" ]]; then  
  read -n 1 -s -r -p "Press a key to continue"  
fi	
