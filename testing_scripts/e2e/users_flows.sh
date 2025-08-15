#!/bin/bash
set -e
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../tests/users.sh"
source "$BASE_DIR/../tests/auth.sh"
source "$BASE_DIR/../tests/files.sh"

function test_sign_up_login_in_get_me_upload_file_download_file_delete_user_logout() {
    echo -e "${YELLOW}🚀 Test e2e: Signup -> Login -> Me -> File(U/D) -> Delete -> Logout ${NO_COLOR}"
    test_create_one_user_auto
    sleep 2
    test_login_and_store_cookie_auto
    sleep 2
    test_get_me
    sleep 2
    test_upload_file_auto
    sleep 2
    test_download_file_auto
    sleep 2
    test_delete_one_user
    sleep 2
    test_logout_and_remove_session_info
}



show_menu (){
echo -e "${CYAN}=== E2E Users Test Menu ===${NO_COLOR}"
echo "1) From SignUp -> Logout"
echo "2) Quit"
read -p "Choose an option: " flow_choice

case "$flow_choice" in
    1) test_sign_up_login_in_get_me_upload_file_download_file_delete_user_logout ;;
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