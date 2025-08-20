#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_PATH="$BASE_DIR/../../instance/market_hall.db"


echo "--------"
echo "$DB_PATH"
echo "--------"


source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"

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

function test_get_all_users_without_session(){
    echo -e "${YELLOW}🚀 Test: get all users without session${NO_COLOR}"
    STATUS_CODE=$(curl -s -o response.json -w "%{http_code}" http://localhost:5000/api/v1/users/)
    # -s deletes progress bar and error messages for the output to be clean
    # -o sends response body into /dev/null instead of outputting it in the screen (console)
    # -w ... tells curl to only display the http code
    if [ "$STATUS_CODE" -eq 200 ]; then
        echo "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        cat response.json
    else
        echo "${RED}❌ Test failed (HTTP $STATUS_CODE)${NO_COLOR}"
        exit 1
    fi
}

function test_get_one_user_as_admin() {
    echo -e "${YELLOW}🚀 Test: get one user as admin (with id:2) ${NO_COLOR}"
    curl_with_cookie_code "http://localhost:5000/api/v1/users/2" \
                        -X GET
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


function test_create_one_not_admin_user_auto() {
      
    echo -e "${YELLOW}🚀 Test: create one simple user (auto)${NO_COLOR}"
    
    curl_with_code "http://localhost:5000/api/v1/users/" \
            -H "Content-Type:application/json" \
            -X POST \
            -d "{\"firstname\":\"simple_user_firstname\",\"lastname\":\"simple_user_lastname\",\"email\":\"simple_user@gmail.com\",\"password\":\"caroline123\"}"

    if [[ "$http_code" -eq 201 ]]; then
        message=$(echo "$body" | jq -r '.message')
        if [[ "$message" == "user created with a cart" ]]; then
            echo -e "${GREEN}✅ Test passed (HTTP 202)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}

function test_create_one_user_auto() {
      
    echo -e "${YELLOW}🚀 Test: create one user auto (auto)${NO_COLOR}"
    
    curl_with_code "http://localhost:5000/api/v1/users/" \
            -H "Content-Type:application/json" \
            -X POST \
            -d "{\"firstname\":\"test_firstname\",\"lastname\":\"test_lastname\",\"email\":\"test@gmail.com\",\"password\":\"caroline123\"}"
 
    if [[ "$http_code" -eq 201 ]]; then
        message=$(echo "$body" | jq -r '.message')
        if [[ "$message" == "user created with a cart" ]]; then
            echo -e "${GREEN}✅ Test passed (HTTP 202)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}


function test_delete_one_simple_user {
    echo -e "${YELLOW}🚀 Test: delete a user ${NO_COLOR}"
    curl_with_cookie_code "http://localhost:5000/api/v1/users/2" \
            -X DELETE \
      
    if [[ "$http_code" -eq 200 ]]; then
        message=$(echo "$body" | jq -r '.message')
        if [[ "$message" == "user deleted" ]]; then
            echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}


function test_delete_one_user {
    echo -e "${YELLOW}🚀 Test: delete a user ${NO_COLOR}"
    curl_with_cookie_code "http://localhost:5000/api/v1/users/1" \
            -X DELETE \
      
    if [[ "$http_code" -eq 200 ]]; then
        message=$(echo "$body" | jq -r '.message')
        if [[ "$message" == "user deleted" ]]; then
            echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}

function test_create_admin {
    
    test_create_one_user_auto

    # Vérifiez la variable DB_PATH
    echo $DB_PATH

    # Testez la commande SQLite directement
    echo "SELECT * FROM users WHERE email='test@gmail.com';" | sqlite3 "$DB_PATH"

    # Testez votre commande UPDATE
    echo "UPDATE users SET role='admin' WHERE email='test@gmail.com';" | sqlite3 "$DB_PATH"
    echo "fin"
    echo -e "${YELLOW}🚀 Test: update role of test user to admin ${NO_COLOR}"
    if [ -f "$DB_PATH" ]; then
        echo -e "${GREEN}market_hall.db exists${NO_COLOR}"
        echo "UPDATE users SET role='admin' WHERE email='test@gmail.com';" | sqlite3 "$DB_PATH"
    else
        echo -e "${GREEN}market_hall.db exists${NO_COLOR}"
        exit 1
    fi
   
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

        if [[ "$http_code" -eq 201 ]]; then
            message=$(echo "$body" | jq -r '.message')
            if [[ "$message" == "user created with a cart" ]]; then
                echo -e "${GREEN}✅ Test passed (HTTP 201)${NO_COLOR}"
            else
                echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
                exit 1
            fi
        else
            echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ No email has been given for the test${NO_COLOR}"
        exit 1
    fi
}




show_menu(){


echo -e "${CYAN}=== API Users Test Menu ===${NO_COLOR}"
echo "1) Get all users without a session"
echo "2) Create one user"
echo "3) Get current user"
echo "4) Create a test user"
echo "5) Delete current user"
echo "6) Create Admin"
echo "7) Get all users as admin"
echo "8) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_get_all_users_without_session ;;
    2) test_create_one_user ;;
    3) test_get_me ;;
    4) test_create_one_user_auto ;;
    5) test_delete_one_user ;;
    6) test_create_admin ;;
    7) test_get_all_users_as_admin ;;
    8) echo "Bye!"; exit 0 ;;
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