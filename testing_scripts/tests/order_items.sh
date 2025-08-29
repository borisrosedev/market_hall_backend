#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"

 
function test_get_all_order_item(){
    
    echo -e "${YELLOW}🚀 Test: get order item test (auto)${NO_COLOR}"
    
    curl_with_cookie_code http://127.0.0.1:5000/api/v1/order_items/1 \
                            -X GET
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}
 

function test_get_all_order_items(){
    echo -e "${YELLOW}🚀 Test: get all orders items ${NO_COLOR}"
    STATUS_CODE=$(curl -s -o response.json -w "%{http_code}" http://127.0.0.1:5000/api/v1/order_items/ -X GET)
    # -s deletes progress bar and error messages for the output to be clean
    # -o sends response body into /dev/null instead of outputting it in the screen (console)
    # -w ... tells curl to only display the http code
    if [ "$STATUS_CODE" -eq 200 ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        cat response.json
    else
        echo -e "${RED}❌ Test failed (HTTP $STATUS_CODE)${NO_COLOR}"
        exit 1
    fi
}

 
function test_create_one_order_item_auto(){
    echo -e "${YELLOW}🚀 Test: create order item (auto) ${NO_COLOR}"
     
    #  Exemple  
    # unit_price_cents = 2999  # 29.99€
    # quantity = 3
    # tax_rate = 0.20  # TVA 20%
    # discount_rate = 0.10  # Remise 10% 
    # subtotal_cents = unit_price_cents * quantity = 2999 * 3  /100= 89.97€
    # discount_cents = subtotal_cents * discount_rate = 899 /100 = 8.99€
    # amount_after_discount = subtotal_cents - discount_cents =  8098 /100 = 80.98€
    # tax_cents = amount_after_discount * tax_rate = 1619 /100 = 16.19€
    # total_cents = amount_after_discount + tax_cents = 9717 /100 = 97.17€
      
    json_data='{
        "order_id": 1, 
        "product_id": 1,
        "sku":"Ref-produit-num0001",
        "product_name" : "Camera1",
        "unit_price_cents" : 2999,
        "quantity" : 3, 
        "subtotal_cents" : 8997,
        "tax_cents" : 1619, 
        "discount_cents" : 899, 
        "total_cents" : 9717, 
        "currency" : "EUR", 
        "variant_json": {
            "color": "red",
            "size": "L", 
            "material": "cotton"
        },
        "metadata_json": {
            "stripe_item_id": "si_1234567890",
            "source": "web"
        }
    }'

    echo "JSON to send:"
    echo "$json_data" | jq .

    curl_with_cookie_code http://127.0.0.1:5000/api/v1/order_items/ \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$json_data"

    if [[ "$http_code" -eq 201 ]]; then
        echo -e "${GREEN}✅ Order item created successfully${NO_COLOR}"
        echo "$body" | jq .
    else
        echo -e "${RED}❌ Failed to create order (HTTP $http_code)${NO_COLOR}"
        echo "$body" | jq .
        exit 1
    fi
}
   
 

show_menu(){

# Menu
echo -e "${CYAN}=== API Orders Items Test Menu ===${NO_COLOR}"
echo "1) Get all order items "
echo "2) Get one order item auto"
echo "3) Create test order item auto"
echo "4) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_get_all_order_items ;; 
    2) test_get_all_order_item ;;
    3) test_create_one_order_item_auto ;; 
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