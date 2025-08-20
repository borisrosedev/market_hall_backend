#!/bin/bash 
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
FILE_PATH="${BASE_DIR}/../../monalisa.png"

source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"
source "$BASE_DIR/../utils/files_utils.sh"



function test_download_file_auto() {
    echo -e "${YELLOW}🚀 Test: download a file (auto) ${NO_COLOR}"
      image_file=$(find_file "uploads" "monalisa") || exit 1
      curl_with_cookie_code http://localhost:5000/static/files/"${image_file}"\
        -F "file=@${FILE_PATH}" \
        -X GET 
    
        if [[ "$http_code" -eq 200 ]]; then       
            echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
            exit 1
        fi
}

function test_download_file(){
    echo -e "${YELLOW}🚀 Test: download a file ${NO_COLOR}"
    read -p "$(echo -e ${CYAN}Image name on the server:${NO_COLOR} ) " image_name

    if [ -n "$image_name" ]; then
        curl_with_cookie_code http://localhost:5000/static/files/$image_name \
        -F "file=@${BASE_DIR}/../../${image_name}" \
        -X GET 
    
        if [[ "$http_code" -eq 200 ]]; then       
            echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
            exit 1
        fi

    else
        echo -e "${RED}❌ No image name has been given for the test${NO_COLOR}"
        exit 1
    fi

}

function test_upload_file_auto () {
    echo -e "${YELLOW}🚀 Test: upload a file (auto) ${NO_COLOR}"
    echo -e "fichier image ${FILE_PATH}"
    curl_with_cookie_code http://localhost:5000/static/files/upload \
        -F "file=@${FILE_PATH};type=image/png" \
        -X POST 
  
    if [[ "$http_code" -eq 200 ]]; then
        message=$(echo "$body" | jq -r '.message')
        if [[ "$message" == "file saved" ]]; then
            echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi

}

function test_upload_file() {
    echo -e "${YELLOW}🚀 Test: upload a file ${NO_COLOR}"
    curl_with_cookie_code http://localhost:5000/static/files/upload \
     -F "file=@${FILE_PATH};type=image/png" \
     -X POST 
  
    if [[ "$http_code" -eq 200 ]]; then
        message=$(echo "$body" | jq -r '.message')
        if [[ "$message" == "file saved" ]]; then
            echo -e "${GREEN}✅ Test passed (HTTP 200)${NO_COLOR}"
        else
            echo -e "${RED}❌ Test failed: unexpected message '$message'${NO_COLOR}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Test failed (HTTP $http_code)${NO_COLOR}"
        exit 1
    fi
}




show_menu (){
# Menu
echo -e "${CYAN}=== API Files Test Menu ===${NO_COLOR}"
echo "1) Upload a file"
echo "2) Download a file"
echo "3) Download monalisa test file automatically"
echo "4) Upload monalisa test file automattically"
echo "5) Quit"
read -p "Choose an option: " choice

case "$choice" in
    1) test_upload_file ;;
    2) test_download_file ;;
    3) test_download_file_auto ;;
    4) test_upload_file_auto ;;
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