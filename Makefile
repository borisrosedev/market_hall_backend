#SHELL := /bin/bash
TESTING_SCRIPTS_FOLDER := testing_scripts
TESTING_SCRIPTS_INDEX_PATH := $(TESTING_SCRIPTS_FOLDER)/index.sh
BACKEND_RUN_SCRIPT := run_flask.sh
CART_TESTS_FILE := $(TESTING_SCRIPTS_FOLDER)/tests/carts.sh
USERS_TESTS_FILE := $(TESTING_SCRIPTS_FOLDER)/tests/users.sh
PRODUCTS_TESTS_FILE := $(TESTING_SCRIPTS_FOLDER)/tests/products.sh
AUTH_TESTS_FILE := $(TESTING_SCRIPTS_FOLDER)/tests/auth.sh
E2E_TESTS_FILE := $(TESTING_SCRIPTS_FOLDER)/e2e/index.sh

.DEFAULT_GOAL := help
.PHONY: help test testv2 api end users prods carts auth

help: ## shows this help
	@grep -e "^[a-zA-Z_-]\+: ## .*$$" $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ": ## "}; {printf "\033[1;36m%-15s\033[0m %s\n", $$1, $$2}'

test: ## shows the menu of API Test
# 	@for f in $(TESTING_SCRIPTS_FOLDER)/*; do \
# 		if [ -f "$$f" ]; then chmod u+x "$$f"; fi; \
# 	done
	@./$(TESTING_SCRIPTS_INDEX_PATH)

testv2: ## shows the menu of API Test
# 	@find testing_scripts -maxdepth 1 -type f -exec chmod u+x {} +
	@./testing_scripts/index.sh

# test la base de donnée 
check_db: ##  checks la fichier check_db.py à la racine du projet
	@python check_db.py

carts: ## runs carts testing
	@chmod u+x $(CART_TESTS_FILE)
	@./$(CART_TESTS_FILE)

prods: ## runs products testing
	@chmod u+x $(PRODUCTS_TESTS_FILE)
	@./$(PRODUCTS_TESTS_FILE)

users: ## runs users testing
	@chmod u+x $(USERS_TESTS_FILE)
	@./$(USERS_TESTS_FILE)

auth: ## runs users testing
	@chmod u+x $(AUTH_TESTS_FILE)
	@./$(AUTH_TESTS_FILE)

end: ## runs end-to-end testing
	@./$(E2E_TESTS_FILE)

api: ## starts the backend 
	@./$(BACKEND_RUN_SCRIPT)
