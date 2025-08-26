#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"

 
function test_get_all_order_addresse(){
    
    echo -e "${YELLOW}🚀 Test: get order addresse test   (auto)${NO_COLOR}"
    
    curl_with_cookie_code http://127.0.0.1:5000/api/v1/order_addresses/1 \
                            -X GET
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}
 

function test_get_all_order_addresses(){
    echo -e "${YELLOW}🚀 Test: get all orders ${NO_COLOR}"
    STATUS_CODE=$(curl -s -o response.json -w "%{http_code}" http://127.0.0.1:5000/api/v1/order_addresses/ -X GET)
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

 
function test_create_one_order_addresse_auto(){
    echo -e "${YELLOW}🚀 Test: create order (auto) ${NO_COLOR}"
     

    curl_with_cookie_code http://127.0.0.1:5000/api/v1/order_addresses/ \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"order_id":1,"type":"shipping","full_name":"Legros LLC","line1":"repudiandae deserunt modi","line2":"deserunt repudiandae modi","city":"Paris","postal_code":"75000","country":"FRANCE","phone":"214-412-7297"}'


    if [[ "$http_code" -eq 201 ]]; then
        echo -e "${GREEN}✅ Order created successfully${NO_COLOR}"
        echo "$body" | jq .
    else
        echo -e "${RED}❌ Failed to create order (HTTP $http_code)${NO_COLOR}"
        echo "$body" | jq .
        exit 1
    fi
}
  
function test_delete_order_addresse(){
    echo -e "${YELLOW}🚀 Test: delete one order addresse ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Order ID:${NO_COLOR} ) " id
     
    if [ -n "$id" ]; then
        curl_with_cookie_code http://localhost:5000/api/v1/order_addresses/"$id"\
            -H "Content-Type:application/json" \
            -X DELETE

        if [[ "$http_code" -eq 200 ]]; then
            message=$(echo "$body" | jq -r '.message')
            if [[ "$message" == "order addresses deleted" ]]; then
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

function test_update_one_order_addresse_auto(){
    
    echo -e "${YELLOW}🚀 Test: update order (auto) ${NO_COLOR}"
      
    curl_with_cookie_code http://localhost:5000/api/v1/order_addresses/1 \
        -X PUT \
        -H "Content-Type: application/json" \
        -d '{"order_id":1,"type":"billing","full_name":"LLC Legros","line1":"repudiandae deserunt modi","line2":"deserunt repudiandae modi","city":"Paris","postal_code":"75000","country":"FRANCE","phone":"214-412-7297"}'


    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}


show_menu(){

# Menu
echo -e "${CYAN}=== API Orders Addresses Test Menu ===${NO_COLOR}"
echo "1) Get all order addresses"
echo "2) Delete one order addresse"
echo "3) Get one order addresse auto"
echo "4) Create test order addresse auto"
echo "5) Update test order addresse auto"
echo "6) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_get_all_order_addresses ;;
    2) test_delete_order_addresse ;;
    3) test_get_all_order_addresse ;;
    4) test_create_one_order_addresse_auto ;;
    5) test_update_one_order_addresse_auto ;;
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