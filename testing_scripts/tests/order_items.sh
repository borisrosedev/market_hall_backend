#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"

 
function test_get_all_order_item(){
    
    echo -e "${YELLOW}🚀 Test: get order item test   (auto)${NO_COLOR}"
    
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
    echo -e "${YELLOW}🚀 Test: get all orders ${NO_COLOR}"
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
    echo -e "${YELLOW}🚀 Test: create order (auto) ${NO_COLOR}"
     
    json_data='{
        "order_id": 1, 
        "product_id": 1,
        "sku":"Ref-produit-num0001",
        "product_name" : "Camera1",
        "unit_price_cents" : 1,
        "quantity" : 1, 
        "subtotal_cents" : 10,
        "tax_cents" : 1, 
        "discount_cents" : 1, 
        "total_cents" : 1, 
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


    if [[ "$http_code" -eq 201 ]]; then
        echo -e "${GREEN}✅ Order created successfully${NO_COLOR}"
        echo "$body" | jq .
    else
        echo -e "${RED}❌ Failed to create order (HTTP $http_code)${NO_COLOR}"
        echo "$body" | jq .
        exit 1
    fi
}
  
function test_delete_order_item(){
    echo -e "${YELLOW}🚀 Test: delete one order item ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Order ID:${NO_COLOR} ) " id
     
    if [ -n "$id" ]; then
        curl_with_cookie_code http://localhost:5000/api/v1/order_items/"$id"\
            -H "Content-Type:application/json" \
            -X DELETE

        if [[ "$http_code" -eq 200 ]]; then
            message=$(echo "$body" | jq -r '.message')
            if [[ "$message" == "order items deleted" ]]; then
                echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
            else
                echo -e "${RED}❌ Unexpected message: '$message'${NO_COLOR}"
                exit 1
            fi
        else
            echo -e "${RED}❌ Failed (HTTP $http_code)${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ No id provided${NO_COLOR}"
        exit 1
    fi  
}

function test_update_one_order_item_auto(){
    
    echo -e "${YELLOW}🚀 Test: update order (auto) ${NO_COLOR}"
      
        json_data='{
        "order_id": 1, 
        "product_id": 1,
        "sku":"Ref-produit-num0001",
        "product_name" : "Camera1",
        "unit_price_cents" : 1,
        "quantity" : 1, 
        "subtotal_cents" : 10,
        "tax_cents" : 1, 
        "discount_cents" : 1, 
        "total_cents" : 1, 
        "currency" : "EUR", 
        "variant_json": {
            "color": "green",
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

    curl_with_cookie_code http://localhost:5000/api/v1/order_items/1 \
        -X PUT \
        -H "Content-Type: application/json" \
        -d "$json_data"

    #echo "HTTP Code: $http_code"
    #echo "Response body:"
    #echo "$body"
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}


show_menu(){

# Menu
echo -e "${CYAN}=== API Orders Items Test Menu ===${NO_COLOR}"
echo "1) Get all order items "
echo "2) Delete one order item"
echo "3) Get one order item auto"
echo "4) Create test order item auto"
echo "5) Update test order item auto"
echo "6) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_get_all_order_items ;;
    2) test_delete_order_item ;;
    3) test_get_all_order_item ;;
    4) test_create_one_order_item_auto ;;
    5) test_update_one_order_item_auto ;;
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