#!/bin/bash


BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"


function response_specific_body_element {
    local body="$1"
    local body_element="$2"
    obj=$(echo "$body" | jq -r ".$body_element")
    echo "$obj"
}

function response_code_and_jq_body {

    local http_code="$1"
    local expected_code="$2"
    local message="$3"
    
    if [[ "$http_code" -eq "$2" ]]; then
        echo -e "${GREEN}✅ $message ${NO_COLOR}"
        echo "$body" | jq .
    else
        echo -e "${RED}❌ not $message (HTTP $http_code)${NO_COLOR}"
        echo "$body" | jq .
        exit 1
    fi
}


function response_code_and_cat_body {
    local http_code="$1"
    local expected_code="$2"
    if [ "$http_code" -eq "$2" ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        cat response.json
    else
        echo -e "${RED}❌ Test failed (HTTP $STATUS_CODE)${NO_COLOR}"
        exit 1
    fi
}

function response_code {
   local http_code="$1"
   local expected_code="$2"

   if [ "$http_code" -eq "$2" ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi


}


function response_code_and_message {

    local http_code="$1"
    local body="$2"
    local expected_code="$3"
    local expected_message="$4"

    if [[ "$http_code" -eq "$expected_code" ]]; then
        message=$(echo "$body" | jq -r '.message')
        if [[ "$message" == "$expected_message" ]]; then
            echo -e "${GREEN}✅ Test passed (HTTP $http_code)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi

}