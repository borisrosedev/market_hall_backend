#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../utils/response_utils.sh"


# ➡️ Updated one information 

function test_update_one_product_price_by_id(){
    echo "=> id: " 
    read -r id 
    echo "=> price_cents: "
    read -r price_cents
    if [ -n "$id" ] && [ -n "$price_cents" ]; then 
        curl_with_cookie_code http://localhost:5000/api/v1/products/$id \
                            -H "Content-Type: application/json" \
                            -d "{\"price_cents\": \"$price_cents\"}" \
                            -X PUT
        response_code "$http_code" 200
    fi
}


# ➡️ Get one product by 1 

function test_get_one_product_by_id(){
    local product_id="$1"
    echo -e "${YELLOW}🚀 Test: get test product $product_id (auto)${NO_COLOR}" 
    curl_with_cookie_code http://localhost:5000/api/v1/products/$product_id \
                            -X GET
    response_code "$http_code" 200
    product=$(response_specific_body_element "$body" product)
    echo "$product"
}

# ➡️ Get all product ( restricted : no)

function test_get_all_products(){
    echo -e "${YELLOW}🚀 Test: get all products ${NO_COLOR}"
    STATUS_CODE=$(curl -s -o response.json -w "%{http_code}" http://localhost:5000/api/v1/products/ -X GET)
    # -s deletes progress bar and error messages for the output to be clean
    # -o sends response body into /dev/null instead of outputting it in the screen (console)
    # -w ... tells curl to only display the http code
    response_code_and_cat_body "$STATUS_CODE" 200 
}


# shellcheck disable=all
function test_create_one_product_auto() {
    local test_product_name="$1"

    echo -e "${YELLOW}🚀 Test: create product $test_product_name (auto) ${NO_COLOR}"
    
    filename_path="${BASE_DIR}/../../testing_images/products/$test_product_name"

    if [ ! -f "$filename_path" ]; then
        echo -e "${RED}❌ File not found: $filename${NO_COLOR}"
        exit 1
    fi

    curl_with_cookie_code http://localhost:5000/api/v1/products/ \
        -X POST \
        -H "Content-Type: multipart/form-data" \
        -F "name=$test_product_name" \
        -F "description=Testing Description" \
        -F "price_cents=100000000" \
        -F "tags=art,antique" \
        -F "quantity=2" \
        -F "sku=ref$test_product_name" \
        -F "file=@$filename_path"

    response_code_and_jq_body "$http_code" 201 "created successfully"
}
 
# ➡️ Create one product manually

#shellcheck disable=all
function test_create_one_product(){
    echo -e "${YELLOW}🚀 Test: create one product ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Name:${NO_COLOR} ) " name
    read -p "$(echo -e ${CYAN}Description:${NO_COLOR} ) " description
    read -p "$(echo -e ${CYAN}price_cents:${NO_COLOR} ) " price_cents
    read -p "$(echo -e ${CYAN}Tags:${NO_COLOR} ) " tags
    read -p "$(echo -e ${CYAN}Quantity:${NO_COLOR} ) " quantity
    read -p "$(echo -e ${CYAN}File path:${NO_COLOR} ) " filename
    read -p "$(echo -e ${CYAN}sku=${NO_COLOR} ) " sku
    #  filename_path="${BASE_DIR}/../../   testing_images/products/${filename}"
    filename_path="../testing_images/products/${filename}" #changé ce path pour viser une image spécifique  

    if [ ! -f "$filename_path" ]; then
        echo -e "${RED}❌ File not found: $filename${NO_COLOR}"
        exit 1
    fi

    curl_with_cookie_code http://localhost:5000/api/v1/products/ \
        -X POST \
        -H "Content-Type: multipart/form-data" \
        -F "name=$name" \
        -F "description=${description:-Default description}" \
        -F "price_cents=$price_cents" \
        -F "tags=$tags" \
        -F "quantity=$quantity" \
        -F "sku=ref$name" \
        -F "file=@$filename_path"

    response_code_and_jq_body "$http_code" 201 "created successfully"
}


# ➡️ Delete one product automatically

function test_delete_one_product_auto (){
    local product_id="$1"
    echo -e "${YELLOW}🚀 Test: delete product $product_id (auto)${NO_COLOR}"
    if [ -n "$product_id" ]; then
        curl_with_cookie_code http://localhost:5000/api/v1/products/$product_id \
            -H "Content-Type:application/json" \
            -X DELETE
            
        response_code_and_message "$http_code" "$body" 200 "product deleted"
    else
        echo -e "${RED}❌ No id provided${NO_COLOR}"
        exit 1
    fi
}


# ➡️ Delete one product

function test_delete_product(){
    echo -e "${YELLOW}🚀 Test: delete one product ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Product ID:${NO_COLOR} ) " id

    if [ -n "$id" ]; then
        curl_with_cookie_code http://localhost:5000/api/v1/products/"$id"\
            -H "Content-Type:application/json" \
            -X DELETE
            
        response_code_and_message "$http_code" "$body" 200 "product deleted"
    else
        echo -e "${RED}❌ No id provided${NO_COLOR}"
        exit 1
    fi
}


# shellcheck disable=all
function test_update_one_product_image_auto(){
    local product_id="$1"
    local new_image_filename="$2"
    echo -e "${YELLOW}🚀 Test: update product image:  $product_id (auto) ${NO_COLOR}"
    
    filename_path="${BASE_DIR}/../../testing_images/products/$new_image_filename"

    if [ ! -f "$filename_path" ]; then
        echo -e "${RED}❌ File not found: $filename${NO_COLOR}"
        exit 1
    fi


    curl_with_cookie_code http://localhost:5000/api/v1/products/1 \
        -X PUT \
        -H "Content-Type: multipart/form-data" \
        -F "name=$product_name" \
        -F "description=Updated Description" \
        -F "price_cents=500" \
        -F "quantity=10" \
        -F "file=@$filename_path"
    
    response_code "$http_code" 200
}



show_menu(){

# Menu
echo -e "${CYAN}=== API Products Test Menu ===${NO_COLOR}"
echo "1) Get all products"
echo "2) Delete one product"
echo "3) Create one product"
echo "4) Create one product (auto) (camera)"
echo "5) Update Test Product (camera) Image (auto)"
echo "6) Delete one product (auto) (camera)"
echo "7) Update one product price by id"
echo "8) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_get_all_products ;;
    2) test_delete_product ;;
    3) test_create_one_product;;
    4) test_create_one_product_auto "camera-1.jpg";;
    5) test_update_one_product_image_auto 1 "pocket-watch.jpg" ;;
    6) test_delete_one_product_auto 1 ;;
    7) test_update_one_product_price_by_id ;;
    8) echo "Bye!"; exit 0 ;;
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