#!/bin/bash


function test_get(){
    curl -X GET http://localhost:5000/api/v1/users/
}

function test_post(){
    curl -H "Content-Type:application/json" \
    -X POST http://localhost:5000/api/v1/users/ \
    -d '{"firstname":"boris","lastname":"rose","email":"boris@gmail.com","password":"caroline123"}'
}


function update_user(){

 curl -H "Content-Type:application/json" \
    -X PUT http://localhost:5000/api/v1/users/1 \
    -d '{"firstname":"boris","lastname":"rose","email":"boris@gmail.com","password":"caroline123"}'
}

function send_file(){
    curl -X POST http://localhost:5000/static/files/upload \
         --cookie "session=eyJfcGVybWFuZW50Ijp0cnVlLCJlbWFpbCI6ImFsZXhAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJ1c2VyX2lkIjoxfQ.aJo4gQ.xqAwm8pMYSkt_BP3LvEFAIuS1eM" \
         -F "file=@./avatar-2.webp;type=image/webp"
}

send_file

