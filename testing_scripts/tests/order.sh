#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"

 
function test_get_one_order_auto(){
    
    echo -e "${YELLOW}🚀 Test: get order test   (auto)${NO_COLOR}"
    
    curl_with_cookie_code http://127.0.0.1:5000/api/v1/orders/1 \
                            -X GET
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}
 

function test_get_all_orders(){
    echo -e "${YELLOW}🚀 Test: get all orders ${NO_COLOR}"
    STATUS_CODE=$(curl -s -o response.json -w "%{http_code}" http://127.0.0.1:5000/api/v1/orders/ -X GET)
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

 
function test_create_one_order_auto(){
    echo -e "${YELLOW}🚀 Test: create order (auto) ${NO_COLOR}"
     

    curl_with_cookie_code http://127.0.0.1:5000/api/v1/orders/ \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"user_id":1,"amounts_cents":10000099,"currency":"USD","status":"created"}'


    if [[ "$http_code" -eq 201 ]]; then
        echo -e "${GREEN}✅ Order created successfully${NO_COLOR}"
        echo "$body" | jq .
    else
        echo -e "${RED}❌ Failed to create order (HTTP $http_code)${NO_COLOR}"
        echo "$body" | jq .
        exit 1
    fi
}
  

function test_create_one_order(){
    echo -e "${YELLOW}🚀 Test: create one order ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}user_id:${NO_COLOR} ) " user_id
    read -p "$(echo -e ${CYAN}amounts_cents:${NO_COLOR} ) " amounts_cents
    read -p "$(echo -e ${CYAN}currency:${NO_COLOR} ) " currency
    read -p "$(echo -e ${CYAN}status:${NO_COLOR} ) " status 
  

    curl_with_cookie_code http://localhost:5000/api/v1/orders/ \
        -X POST \
        -H "Content-Type: application/json" \
        -F "user_id=$user_id" \
        -F "amounts_cents=$amounts_cents" \
        -F "currency=$currency" \
        -F "status=$status" 

    if [[ "$http_code" -eq 201 ]]; then
        echo -e "${GREEN}✅ Order created successfully${NO_COLOR}"
        echo "$body" | jq .
    else
        echo -e "${RED}❌ Failed to create order (HTTP $http_code)${NO_COLOR}"
        echo "$body" | jq .
        exit 1
    fi
}

function test_delete_order(){
    echo -e "${YELLOW}🚀 Test: delete one order ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Order ID:${NO_COLOR} ) " id
     
    if [ -n "$id" ]; then
        curl_with_cookie_code http://localhost:5000/api/v1/orders/"$id"\
            -H "Content-Type:application/json" \
            -X DELETE

        if [[ "$http_code" -eq 200 ]]; then
            message=$(echo "$body" | jq -r '.message')
            if [[ "$message" == "order deleted" ]]; then
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

function test_update_one_order_auto(){
    
    echo -e "${YELLOW}🚀 Test: update order (auto) ${NO_COLOR}"
      
    curl_with_cookie_code http://localhost:5000/api/v1/orders/1 \
        -X PUT \
        -H "Content-Type: application/json" \
        -d '{"user_id":1,"amounts_cents":5000000000,"currency":"CHN","status":"created"}'
 

    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}


show_menu(){

# Menu
echo -e "${CYAN}=== API Orders Test Menu ===${NO_COLOR}"
echo "1) Get all order"
echo "2) Delete one order"
echo "3) Get one order auto"
echo "4) Create test order auto"
echo "5) Update test order auto"
echo "6) Create one order" 
echo "7) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_get_all_orders ;;
    2) test_delete_order ;;
    3) test_get_one_order_auto ;;
    4) test_create_one_order_auto ;;
    5) test_update_one_order_auto ;;
    6) test_create_one_order;;
    7) echo "Bye!"; exit 0 ;;
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