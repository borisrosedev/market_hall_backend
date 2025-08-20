#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_PATH="$BASE_DIR/../../instance/market_hall.db"

source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../utils/response_utils.sh"

echo -e "${YELLOW}🚀 Test Suite: Users${NO_COLOR}"

function test_get_all_users_as_admin(){
      
    echo -e "${YELLOW}🚀 Test: get all users as admin ${NO_COLOR}"
    
    curl_with_cookie_code http://localhost:5000/api/v1/users/ \
                    -X GET
    if [[ "$http_code" -eq 200 ]]; then  
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        response=$(echo "$body" | jq .)
        echo "$response"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi

}




function test_get_me {
    echo -e "${YELLOW}🚀 Test: get current user ${NO_COLOR}"
    curl_with_cookie_code "http://localhost:5000/api/v1/users/me" \
                        -X GET \
    
    if [[ "$http_code" -eq 200 ]]; then
            user_id=$(echo "$body" | jq -r '.id')
            if [[ "$user_id" ]]; then
                user=$(echo "$body" | jq)
                echo "$user"
            else
                echo -e "${RED}❌ Test failed: unexpected message '$(echo "$body" | jq -r '.message')'${NO_COLOR}"
                exit 1
            fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}


function test_create_one_user_auto() {
    local firstname="$1"
    echo -e "${YELLOW}🚀 Test: create one user auto (auto)${NO_COLOR}"
    
    curl_with_code "http://localhost:5000/api/v1/users/" \
            -H "Content-Type:application/json" \
            -X POST \
            -d "{\"firstname\":\"$firstname\",\"lastname\":\"dupont\",\"email\":\"$firstname@gmail.com\",\"password\":\"caroline123\"}"
 
    response_code_and_message "$http_code" "$body" 201 "user created with a cart" 
}



function test_delete_one_simple_user {
    echo -e "${YELLOW}🚀 Test: delete a user ${NO_COLOR}"
    curl_with_cookie_code "http://localhost:5000/api/v1/users/2" \
            -X DELETE \
      
    response_code_and_message "$http_code" "$body" 200 "user deleted" 
}

# shellcheck disable=all
function test_delete_one_user {
    local user_id="$1"
    echo -e "${YELLOW}🚀 Test: delete a user ${NO_COLOR}"
    curl_with_cookie_code "http://localhost:5000/api/v1/users/$user_id" \
            -X DELETE \

    response_code_and_message "$http_code" "$body" 200 "user deleted" 
    
}



function test_create_one_user {
    echo -e "${YELLOW}🚀 Test: create a user ${NO_COLOR}"
    echo -e "${CYAN}What is the email of the new user?${NO_COLOR}"
    read email

    if [ -n "$email" ]; then
        curl_with_code "http://localhost:5000/api/v1/users/" \
            -H "Content-Type:application/json" \
            -X POST \
            -d "{\"firstname\":\"Susie\",\"lastname\":\"Bernard\",\"email\":\"$email\",\"password\":\"caroline123\"}"

        response_code_and_message "$http_code" "$body" 201 "user created with a cart" 
    else
        echo -e "${RED}❌ No email has been given for the test${NO_COLOR}"
        exit 1
    fi
}




show_menu(){


echo -e "${CYAN}=== API Users Test Menu ===${NO_COLOR}"
echo "1) Create one user"
echo "2) Get current user"
echo "3) Create a test user (auto)"
echo "4) Delete one user"
echo "5) Get all users as admin"
echo "6) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_create_one_user ;;
    2) test_get_me ;;
    3) test_create_one_user_auto "test_user" ;;
    4) test_delete_one_user ;;
    5) test_get_all_users_as_admin ;;
    6) echo "Bye!"; exit 0 ;;
    *) echo -e "${RED}Invalid choice${NO_COLOR}"; exit 1 ;;
esac

}

main() {
  show_menu
}

# --- guard ---
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi