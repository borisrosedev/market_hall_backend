#!/bin/bash 

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COOKIE_FILE="$BASE_DIR/../cookies.txt"

curl_with_code() {
    #local variable named url
    local url="$1" # $1 first argument passed to the function
    shift #remove $1 from $@.
    #create a tempory unique file
    local tmpfile=$(mktemp)
    http_code=$(curl -s -o "$tmpfile" -w "%{http_code}" "$@" "$url")
    body=$(cat "$tmpfile")
    rm "$tmpfile"
}

curl_with_copy_cookie_code(){
    local url="$1"
    shift
    local tmpfile=$(mktemp)
    http_code=$(curl -s -c "$COOKIE_FILE" -o "$tmpfile" -w "%{http_code}" "$@" "$url")
    body=$(cat "$tmpfile")
    rm "$tmpfile"
}

curl_with_cookie_code() {
    local url="$1"
    shift
    local tmpfile=$(mktemp)
    http_code=$(curl -s -b "$COOKIE_FILE" -o "$tmpfile" -w "%{http_code}" "$@" "$url")
    body=$(cat "$tmpfile")
    rm "$tmpfile"
}