#!/bin/bash


function test_get_ById_product(){
    curl -X GET http://localhost:5000/api/v1/products/getBy/5
}


function test_update_product(){
    curl -H "Content-Type:application/json" \
    -X PUT http://localhost:5000/api/v1/products/update/5 \
    -d '{"name":"test","description":"test","price":100,"quantity":10}'
}

function test_create_product_camera1(){
    curl -X POST http://localhost:5000/api/v1/products/ \
    -H "Content-Type: multipart/form-data" \
    -F "name=Camera1" \
    -F "description=Testing Description" \
    -F "price=1000000000" \
    -F "tags=painting,art" \
    -F "quantity=1" \
    -F "file=@./testing_images/products/camera-1.jpg"
}


function test_create_product_camera2(){
    curl -X POST http://localhost:5000/api/v1/products/ \
    -H "Content-Type: multipart/form-data" \
    -F "name=Camera2" \
    -F "description=Testing Description" \
    -F "price=20000" \
    -F "tags=painting,art" \
    -F "quantity=1" \
    -F "file=@./testing_images/products/camera-2.jpg"
}

function test_create_product_pocket-watch(){
    curl -X POST http://localhost:5000/api/v1/products/ \
    -H "Content-Type: multipart/form-data" \
    -F "name=Pocket watch" \
    -F "description=Testing Description" \
    -F "price=5240000" \
    -F "tags=painting,art" \
    -F "quantity=1" \
    -F "file=@./testing_images/products/pocket-watch-1.jpg"
}
 
function test_file_upload (){
    curl -X POST http://localhost:5000/static/files/upload \
    -F "file=@./testing_images/products/pocket-watch-1.jpg"
    
    curl -X POST http://localhost:5000/static/files/upload  
    
}

function test_file_upload_image_type (){
    curl -X POST http://localhost:5000/static/files/upload \
    -F "file=@./testing_images/products/camera-1.jpg"
    
    curl -X POST http://localhost:5000/static/files/upload \
    -F "file=@./testing_images/products/camera-2.jpg"
}


function test_create_order(){
    curl -X POST http://127.0.0.1:5000/api/v1/orders/ \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"amounts_cents":10000099,"currency":"USD","status":"created"}'

   
    curl -X POST http://127.0.0.1:5000/api/v1/orders/ \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"amounts_cents":5000000000000,"currency":"JPY","status":"created"}'

    curl -X POST http://127.0.0.1:5000/api/v1/orders/ \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"amounts_cents":10099,"currency":"DBP","status":"created"}'
           
}

function test_create_order_adresses(){
    curl -X POST http://127.0.0.1:5000/api/v1/orders/ \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"amounts_cents":10000099,"currency":"USD","status":"created"}'

    curl -X POST http://127.0.0.1:5000/api/v1/order_addresses/ \
    -H "Content-Type: application/json" \
    -d '{"order_id":1,"type":"shipping","full_name":"Cpy adr","line1":"Rue de la compagnie","line2":"1 etage","city":"Paris","postal_code":"75000","country":"FRANCE","phone":"070125832321"}'
}
#test_post
#test_get_all_product 
#test_get_ById_product
#test_update_product

#test_create_product_camera1
#test_create_product_camera2
#test_create_product_pocket-watch

#test_file_upload
#test_file_upload_image_type

#test_create_order
test_create_order_adresses
