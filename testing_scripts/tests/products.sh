#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"


function test_get_all_products(){
    echo -e "${YELLOW}🚀 Test: get all products ${NO_COLOR}"
    STATUS_CODE=$(curl -s -o response.json -w "%{http_code}" http://localhost:5000/api/v1/products/)
    # -s deletes progress bar and error messages for the output to be clean
    # -o sends response body into /dev/null instead of outputting it in the screen (console)
    # -w ... tells curl to only display the http code
    if [ "$STATUS_CODE" -eq 200 ]; then
        echo "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        cat response.json
    else
        echo "${RED}❌ Test failed (HTTP $STATUS_CODE)${NO_COLOR}"
        exit 1
    fi
}

function test_create_one_product(){
    echo -e "${YELLOW}🚀 Test: create one product ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Name:${NO_COLOR} ) " name
    read -p "$(echo -e ${CYAN}Description:${NO_COLOR} ) " description
    read -p "$(echo -e ${CYAN}Price:${NO_COLOR} ) " price
    read -p "$(echo -e ${CYAN}Tags:${NO_COLOR} ) " tags
    read -p "$(echo -e ${CYAN}Quantity:${NO_COLOR} ) " quantity
    read -p "$(echo -e ${CYAN}File path:${NO_COLOR} ) " filename

    if [ ! -f "$filename" ]; then
        echo -e "${RED}❌ File not found: $filename${NO_COLOR}"
        exit 1
    fi

    curl_with_cookie_code http://localhost:5000/api/v1/products/ \
        -X POST \
        -H "Content-Type: multipart/form-data" \
        -F "name=$name" \
        -F "description=${description:-Default description}" \
        -F "price=$price" \
        -F "tags=$tags" \
        -F "quantity=$quantity" \
        -F "file=@$filename"

    if [[ "$http_code" -eq 201 ]]; then
        echo -e "${GREEN}✅ Product created successfully${NO_COLOR}"
        echo "$body" | jq .
    else
        echo -e "${RED}❌ Failed to create product (HTTP $http_code)${NO_COLOR}"
        echo "$body" | jq .
        exit 1
    fi
}

function test_delete_product(){
    echo -e "${YELLOW}🚀 Test: delete one product ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Product ID:${NO_COLOR} ) " id

    if [ -n "$id" ]; then
        curl_with_cookie_code http://localhost:5000/api/v1/products/"$id"\
            -H "Content-Type:application/json" \
            -X DELETE

        if [[ "$http_code" -eq 200 ]]; then
            message=$(echo "$body" | jq -r '.message')
            if [[ "$message" == "product deleted" ]]; then
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



show_menu(){

# Menu
echo -e "${CYAN}=== API Products Test Menu ===${NO_COLOR}"
echo "1) Get all products without a session"
echo "2) Delete one product"
echo "3) Create one product"
echo "4) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_get_all_products ;;
    2) test_delete_product ;;
    3) test_create_one_product ;;
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