#!/bin/bash

while true  
do
    read -p "Entrez un nombre (0 pour quitter): " num
    
    if (( num == 0 ))
    then
        echo "Au revoir!"
        break  # Sort de la boucle
    fi
    
    echo "Vous avez entré: $num"
done
