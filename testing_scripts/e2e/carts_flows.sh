#!/bin/bash
set -e
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../tests/users.sh"
source "$BASE_DIR/../tests/auth.sh"
source "$BASE_DIR/../tests/files.sh"
source "$BASE_DIR/../tests/products.sh"
source "$BASE_DIR/../tests/carts.sh"





function test_admin_create_update_product () {
  echo -e "$GREEN Admin -> Create -> Update Product -> Logout Test $NO_COLOR"
  test_login_and_store_cookie_auto  "admin_boris@gmail.com"
  sleep 2
  test_create_one_product_auto "camera-2.jpg"
  sleep 2
  test_update_one_product_image_auto 2 "pocket-watch-1.jpg"
  sleep 2
  test_logout_and_remove_session_info
}

function test_create_user_get_cart_get_product_add_product_to_cart_update_add_another_get_cart_delete_one_logout () {
  echo -e "$(CYAN)Create User -> Login -> Get Product -> Add -> Add -> Update -> Cart -> Delete -> Logout $(NO_COLOR)"
  test_create_one_user_auto "max"
  sleep 2
  test_login_and_store_cookie_auto "max@gmail.com"
  sleep 2
  test_get_one_product_by_id 1
  sleep 2
  test_add_item_to_cart 8 1 1
  sleep 2
  test_update_cart_item 8 1 0
  sleep 2
  test_add_item_to_cart 8 3 1
  sleep 2
  test_add_item_to_cart 8 2 1
  sleep 2
  test_get_current_user_cart
  sleep 2
  test_delete_cart_item 8 1
  sleep 2
  test_get_current_user_cart
  sleep 2
  test_logout_and_remove_session_info
}


function test_from_admin_login_to_user_logout() {
  test_admin_create_update_product
  test_create_user_get_cart_get_product_add_product_to_cart_update_add_another_get_cart_delete_one_logout 
}


show_menu (){
echo -e "${CYAN}=== E2E Carts Test Menu ===${NO_COLOR}"
echo "1) From Admin Login -> User Logout"
echo "2) Quit"
read -p "Choose an option: " flow_choice

case "$flow_choice" in
    1) test_from_admin_login_to_user_logout ;;
    2) echo "Bye!"; exit 0 ;;
    *) echo -e "${RED}Invalid choice${NO_COLOR}"; exit 1 ;;
esac
}



# --- guard ---
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi