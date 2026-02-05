#!/bin/bash

produits=("Pomme" "Banane" "Orange" "raisin" )

echo "Liste des produits "

for i in ${!produits[*]}
do 
	echo " $((i+1)). ${produits[i]} " 
done 
