#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/order.sh"
source "$BASE_DIR/order_addresses.sh"
source "$BASE_DIR/order_items.sh"
  
show_menu(){

# Menu
echo -e "${CYAN}=== API Orders Test Menu ===${NO_COLOR}"
echo "1) Orders"
echo "2) Order addresses"
echo "3) Order items"
echo "4) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) "$BASE_DIR/order.sh" ;;
    2) "$BASE_DIR/order_addresses.sh" ;;
    3) "$BASE_DIR/order_items.sh" ;;
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