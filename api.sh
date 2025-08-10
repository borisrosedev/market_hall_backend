#!/bin/bash


function test_get(){
    curl -X GET http://localhost:5000/api/v1/users/
}

function test_post(){
    curl -H "Content-Type:application/json" \
    -X POST http://localhost:5000/api/v1/users/ \
    -d '{"firstname":"boris","lastname":"rose","email":"boris@gmail.com","password":"caroline123"}'
}

test_post
