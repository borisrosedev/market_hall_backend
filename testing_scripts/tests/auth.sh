#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../utils/response_utils.sh"


# ➡️ Logout and Remove Session Info

function test_logout_and_remove_session_info {
    echo -e "${YELLOW}🚀 Test: Logout user ${NO_COLOR}"
    curl_with_cookie_code  http://localhost:5000/api/v1/auth/logout \
                        -X GET   

    response_code_and_message "$http_code" "$body" 200 "session end"
}


# ➡️ Login & Store Cookie
# shellcheck disable=all
function test_login_and_store_cookie_auto {
    local email="$1"
    echo -e "${YELLOW}🚀 Test: Login user & Save cookie (auto) ${NO_COLOR}"
    curl_with_copy_cookie_code http://localhost:5000/api/v1/auth/login \
                                    -H "Content-Type: application/json" \
                                    -X POST \
                                    -d "{\"email\":\"$email\",\"password\":\"caroline123\"}"
          
    response_code_and_message "$http_code" "$body" 200 "session started"

}

function test_login_and_store_cookie {
    echo -e "${YELLOW}🚀 Test: Login user & Store cookie ${NO_COLOR}"
    echo -e "------------------Question 1/2-----------------------\n"
    echo -e "${CYAN}What is the email of the user?${NO_COLOR}"
    read email
    echo -e "-------------------Question 2/2----------------------\n"
    echo -e "${CYAN}What is the password of the user?${NO_COLOR}"
    read password

    if [ -n "$email" ]; then
        if [ -n "$password" ]; then 
            curl_with_copy_cookie_code http://localhost:5000/api/v1/auth/login \
                                    -H "Content-Type: application/json" \
                                    -X POST \
                                    -d "{\"email\":\"$email\",\"password\":\"$password\"}"
          
            response_code_and_message "$http_code" "$body" 200 "session started"
            echo -e "${GREEN}✅ Cookie saved in cookies.txt${NO_COLOR}"
        else 
            echo -e "${RED}❌ No password has been given for the test${NO_COLOR}"
            exit 1
        
        fi 
    else 
        echo -e "${RED}❌ No email has been given for the test${NO_COLOR}"
        exit 1
    fi
}



show_menu() {
# Menu
echo -e "${CYAN}=== API Auth Test Menu ===${NO_COLOR}"
echo "1) Login & Save a session cookie"
echo "2) Logout & Remove session info"
echo "3) Login test user & Save their cookie"
echo "4) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_login_and_store_cookie ;;
    2) test_logout_and_remove_session_info;;
    3) test_login_and_store_cookie_auto ;;
    4) echo "Bye!"; exit 0 ;;
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