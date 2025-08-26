#!/bin/bash
set -e
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../tests/users.sh"
source "$BASE_DIR/../tests/auth.sh"
source "$BASE_DIR/../tests/files.sh"
source "$BASE_DIR/../tests/products.sh"
source "$BASE_DIR/../tests/admins.sh"
source "$BASE_DIR/../tests/order.sh"
source "$BASE_DIR/../tests/order_addresses.sh"

function test_create_login_store_cookie_get_me_create_get_update_product_get_updated_data_create_new_user_get_all_users_get_my_account_logout() {
    echo -e "${YELLOW}🚀 Test e2e: Login -> Create Prod -> Get it -> Update it -> Get all -> Logout -> Get all ${NO_COLOR}"
    test_create_one_user_auto "user_test"
    sleep 2
    test_create_future_admin_auto "admin_test"
    sleep 2
    test_update_role_to_admin "admin_test"
    sleep 2
    test_login_and_store_cookie_auto "admin_test@gmail.com"
    sleep 2
    test_login_and_store_cookie_auto "admin_test@gmail.com"
    sleep 2
    test_get_me 
    sleep 2 
    test_create_one_product_auto "camera-1.jpg"
    sleep 2 
    test_create_one_product_auto "camera-2.jpg"
    sleep 2
    test_create_one_product_auto "pocket-watch-1.jpg"
    sleep 2
    test_get_all_users_as_admin
    sleep 2
    test_get_all_products
    sleep 2
    
    test_create_one_order_auto
    sleep 2
    test_get_all_orders
    sleep 2
    test_create_one_order_addresse_auto
    sleep 2 
    test_get_all_order_addresses
    sleep 2
    test_logout_and_remove_session_info
    echo -e "${YELLOW}🎉 Test e2e: End of the test ${NO_COLOR}"
}


show_menu (){
echo -e "${CYAN}=== E2E Admin init bd Test Menu ===${NO_COLOR}"
echo "1) From Login -> Insert Test -> Logout "
echo "2) Quit"
read -p "Choose an option: " flow_choice

case "$flow_choice" in
    1) test_create_login_store_cookie_get_me_create_get_update_product_get_updated_data_create_new_user_get_all_users_get_my_account_logout ;;
    2) echo "Bye!"; exit 0 ;;
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