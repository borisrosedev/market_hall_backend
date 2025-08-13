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

function test_send_file(){
    curl -X POST http://localhost:5000/static/files/upload \
         --cookie "session=eyJfcGVybWFuZW50Ijp0cnVlLCJlbWFpbCI6ImFsZXhAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJ1c2VyX2lkIjoxfQ.aJo4gQ.xqAwm8pMYSkt_BP3LvEFAIuS1eM" \
         -F "file=@./avatar-2.webp;type=image/webp"
}

function test_update_product(){
    curl -H "Content-Type:application/json" \
    -X PUT http://localhost:5000/api/v1/products/update/5 \
    -d '{"name":"test","description":"test","price":100,"quantity":10}'
}

function test_create_product_daVinci(){
    curl -X POST http://localhost:5000/api/v1/products/ \
    -H "Content-Type: multipart/form-data" \
    -F "name=Mona Lisa" \
    -F "description=Painting of the most famous artist Leonardo DaVinci" \
    -F "price=1000000000" \
    -F "tags=painting,art" \
    -F "quantity=1" \
    -F "file=@./monalisa.png"
}


function test_create_product_vermeer(){
    curl -X POST http://localhost:5000/api/v1/products/ \
    -H "Content-Type: multipart/form-data" \
    -F "name=La Jeune Fille à la perle" \
    -F "description=Artist Johannes Vermeer" \
    -F "price=1540000" \
    -F "tags=painting,art" \
    -F "quantity=1" \
    -F "file=@./la-jeune-fille-a-perle.jpg"
}

function test_create_product_botticelli(){
    curl -X POST http://localhost:5000/api/v1/products/ \
    -H "Content-Type: multipart/form-data" \
    -F "name=La naissance de Vénus" \
    -F "description=La Naissance de Vénus est un tableau de Sandro Botticelli, peint vers 1482-1485 et conservé à la galerie des Offices. Il a été peint selon la technique de la tempera. Il représente la déesse Vénus arrivant sur le rivage après sa naissance. Artist  Sandro Botticelli" \
    -F "price=5240000" \
    -F "tags=painting,art" \
    -F "quantity=1" \
    -F "file=@./la_nascita_di_Venere.gif"
}

function test_for_understand(){
    curl -X GET http://localhost:5000/static/files/la_nascita_di_Venere-20250812-115630-1f2e7ac828ae4d9d884bc4f480b44aa9.gif
}

function test_file (){
    curl -X POST http://localhost:5000/static/files// \ 
    -F "file=@.\upload/monalisa.png"
}

#test_post
#test_get_all_product 
# test_get_ById_product
# test_update_product

#test_create_product_daVinci
#test_create_product_vermeer
#test_create_product_botticelli
#test_file 
 


test_for_understand
