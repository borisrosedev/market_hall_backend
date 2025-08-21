#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../utils/response_utils.sh"

# shellcheck disable=all
function test_add_item_to_cart {
  echo "🚀 Add Item To Cart Test"
  local cart_id="$1"
  local product_id="$2"
  local quantity="$3"
  curl_with_cookie_code http://localhost:5000/api/v1/carts/$cart_id/items/$product_id?quantity=$quantity \
                  -X GET
  response_code_and_message "$http_code" "$body" 200 "cart item added"
}

# shellcheck disable=all
function test_update_cart_item {
  echo "🚀 Update Item In Cart Test"
  local cart_id="$1"
  local product_id="$2"
  local quantity="$3"
  curl_with_cookie_code http://localhost:5000/api/v1/carts/$cart_id/items/$product_id?quantity=$quantity \
                  -X GET
  response_code_and_message "$http_code" "$body" 200 "cart item quantity updated"
  
}


# shellcheck disable=all
function test_delete_cart_item {
    echo "🚀 Delete Item In Cart Test"
  local cart_id="$1"
  local product_id="$2"
  curl_with_cookie_code http://localhost:5000/api/v1/carts/$cart_id/items/$product_id \
                  -X DELETE
  response_code_and_message "$http_code" "$body" 200 "cart item deleted"
}

# shellcheck disable=all
function test_get_current_user_cart {
  echo "🚀 Get Current User Cart Test"
  curl_with_cookie_code http://localhost:5000/api/v1/carts/me \
                  -X GET
  response_code_and_jq_body "$http_code" 200 "all good"
}


show_menu(){


echo -e "${CYAN}=== API Carts Test Menu ===${NO_COLOR}"
echo "1) Add item to a cart"
echo "2) Update cart item"
echo "3) Delete cart item"
echo "4) Get Current User Cart"
echo "5) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_add_item_to_cart ;;
    2) test_update_cart_item ;;
    3) test_delete_cart_item ;;
    4) test_get_current_user_cart ;;
    5) echo "Bye!"; exit 0 ;;
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