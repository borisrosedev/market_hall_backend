#!/bin/bash
set -e
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../tests/admins.sh"
source "$BASE_DIR/../tests/users.sh"
source "$BASE_DIR/../tests/auth.sh"
source "$BASE_DIR/../tests/files.sh"
source "$BASE_DIR/../tests/products.sh"


function test_e2e_admin_login_create_get_update_deleta_logout {
    test_create_future_admin_auto "admin_test"
    sleep 2
    test_update_role_to_admin "admin_test"
    sleep 2
    test_login_and_store_cookie_auto "admin_test@gmail.com"
    sleep 2
    test_create_one_product_auto "camera-1.jpg"
    sleep 2
    test_get_one_product_by_id 1
    sleep 2
    test_update_one_product_image_auto 1 "camera-2.jpg"
    sleep 2
    test_get_one_product_by_id 1
    sleep 2
    test_delete_one_product_auto 1
    sleep 2
    test_logout_and_remove_session_info
    sleep 2
    test_delete_one_user 1

}


show_menu (){
echo -e "${CYAN}=== E2E Users Test Menu ===${NO_COLOR}"
echo "1) [admin] from create to deletion"
echo "2) Quit"
read -p "Choose an option: " flow_choice

case "$flow_choice" in
    1) test_e2e_admin_login_create_get_update_deleta_logout;;
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