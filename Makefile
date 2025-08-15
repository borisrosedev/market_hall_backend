#SHELL := /bin/bash
TESTING_SCRIPTS_FOLDER := testing_scripts
TESTING_SCRIPTS_INDEX_PATH := $(TESTING_SCRIPTS_FOLDER)/index.sh
BACKEND_RUN_SCRIPT := run_flask.sh


.DEFAULT_GOAL := help
.PHONY: help test testv2 api

help: ## shows this help
	@grep -e "^[a-zA-Z_-]\+: ## .*$$" $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ": ## "}; {printf "\033[1;36m%-15s\033[0m %s\n", $$1, $$2}'

test: ## shows the menu of API Test
	@for f in $(TESTING_SCRIPTS_FOLDER)/*; do \
		if [ -f "$$f" ]; then chmod u+x "$$f"; fi; \
	done
	@./$(TESTING_SCRIPTS_INDEX_PATH)

testv2: ## shows the menu of API Test
	@find testing_scripts -maxdepth 1 -type f -exec chmod u+x {} +
	@./testing_scripts/index.sh

api: ## starts the backend 
	@./$(BACKEND_RUN_SCRIPT)