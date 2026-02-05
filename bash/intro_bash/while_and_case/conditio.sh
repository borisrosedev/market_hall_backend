#!/bin/bash

while [[ -f "file.txt" ]]
do
    echo "file.txt existe"
    echo "Suppression..."
    rm file.txt
    
    echo "Récration de fichier " 
    touch file.txt
    echo "Le fichier est recréé " 
    sleep 1
done


echo "file.txt n'existe plus"
