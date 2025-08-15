#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../constants/colors.sh"
source "$BASE_DIR/../utils/curl_utils.sh"



show_menu(){
  echo -e "${CYAN}=== END TO END Test Menu ===${NO_COLOR}"
  echo "1) Users"
  echo "2) Admins"
  echo "3) Quit"
  read -p "Choose an option: " e2e_choice

  case "$e2e_choice" in
      1) "$BASE_DIR/users_flows.sh" ;;
      2) "$BASE_DIR/admins_flows.sh" ;;
      3) echo "Bye!"; exit 0 ;;
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