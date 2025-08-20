#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_PATH="$BASE_DIR/../../instance/market_hall.db"

source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../utils/response_utils.sh"

echo -e "${YELLOW}🚀 Test Suite: Admins${NO_COLOR}"

# ➡️ Update user role into the db




function test_update_role_to_admin() {
    
    local firstname="$1"
    echo -e "${YELLOW}🚀 Test: update role of $firstname ${NO_COLOR}"
    if [ -f "$DB_PATH" ]; then
        echo "UPDATE users SET role='admin' WHERE email='$firstname@gmail.com';" | sqlite3 "$DB_PATH"
        echo "✅ $firstname's role has been updated successfully"
    else
        echo -e "${GREEN}market_hall.db exists${NO_COLOR}"
        exit 1
    fi
   
}

# ➡️ Create future_admin

function test_create_future_admin_auto() {

    local firstname="$1"

    echo -e "${YELLOW}🚀 Test: create future admin $firstname (auto) ${NO_COLOR}"
    
    curl_with_code "http://localhost:5000/api/v1/users/" \
            -H "Content-Type:application/json" \
            -X POST \
            -d "{\"firstname\":\"$firstname\",\"lastname\":\"dupont\",\"email\":\"$firstname@gmail.com\",\"password\":\"caroline123\"}"
 
    response_code_and_message "$http_code" "$body" 201 "user created with a cart" 
}



# ➡️ Create Batch 4 admins

function create_batch_4_admins {

   admins=('admin_boris'  'admin_caroline' 'admin_pierre'  'admin_lila')

   for admin in "${admins[@]}"
   do
        test_create_future_admin_auto "$admin"
        sleep 1
        test_update_role_to_admin "$admin"

   done


}


show_menu() {
# Menu
echo -e "${CYAN}=== API Admins Test Menu ===${NO_COLOR}"
echo "1) Create 4 admins"
echo "2) Update role to admin (auto)"
echo "3) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) create_batch_4_admins ;;
    2) test_update_role_to_admin "alex" ;;
    3) echo "Bye!"; exit 0 ;;  
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