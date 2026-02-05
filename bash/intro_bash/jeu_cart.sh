#!/bin/bash 
# tableau de couleurs 
couleurs=("carreau" "coeur" "pinque" "trefle " )

# tableau de valeurs 
valeurs=( "5"  "6" "7" "8" "valet" "dame"  "roi" "as" )

# tier une couleur aléatore
couleur_aleatoire=$(( RANDOM % ${#couleurs[*]} )) 

#tire une valeur aléatoire 

valeur_aleatoire=$(( RANDOM % ${#valeurs[*]}))

#afficher les cartes tirée 

echo " ${valeurs[valeur_aleatoire]} de ${couleurs[couleur_aleatoire]}"
