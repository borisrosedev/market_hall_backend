#!/bin/bash
set -e
BASE_DIR="$(dirname "$0")"
source "$BASE_DIR/constants/colors.sh"


show_menu(){
echo -e "${CYAN}=== API Test Menu ===${NO_COLOR}"
echo "1) Products"
echo "2) Users"
echo "3) Files"
echo "4) Auth"
echo "5) End To End"
echo "6) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) "$BASE_DIR/tests/products.sh" ;;
    2) "$BASE_DIR/tests/users.sh" ;;
    3) "$BASE_DIR/tests/files.sh" ;;
    4) "$BASE_DIR/tests/auth.sh" ;;
    5) "$BASE_DIR/e2e/index.sh" ;;
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