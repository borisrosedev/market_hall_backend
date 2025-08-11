#!/bin/bash


function test_get(){
    curl -X GET http://localhost:5000/api/v1/users/
}

function test_post(){
    curl -H "Content-Type:application/json" \
    -X POST http://localhost:5000/api/v1/users/ \
    -d '{"firstname":"boris","lastname":"rose","email":"boris@gmail.com","password":"caroline123"}'
}

function test_get_all_product(){
    curl -X GET http://localhost:5000/api/v1/products/
}
function test_get_ById_product(){
    curl -X GET http://localhost:5000/api/v1/products/getBy/5
}
function test_delete_product(){
    curl -X GET http://localhost:5000/api/v1/products/delete/4
}

function test_update_product(){
    curl -H "Content-Type:application/json" \
    -X PUT http://localhost:5000/api/v1/products/update/5 \
    -d '{"name":"test","description":"test","price":100,"quantity":10}'
}
#test_post
#test_get_all_product 
test_get_ById_product
test_update_product

