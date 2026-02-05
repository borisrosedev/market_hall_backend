#!/bin/bash

couleurs=( "rouge" "bleu" "vert" "jaune" "noir" )

#Choisir un indice aléatoire 
indice=$(( RANDOM % ${#couleurs[*]} ))

echo "Couleur trié au hasard : ${couleurs[indice]} "

