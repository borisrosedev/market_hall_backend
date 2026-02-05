# == les tableaux 
# pour déclare un talbeau avec des éléments de dans : declare -a animaux=( "chat" "chien" "souris" "oiseau" )
# Déclarer un tableau avec des indexs précis : declare -a notes=( [0]="Alice" [2]="Bob" [5]="hota" )
# Accèder à une élément de tableau :
#echo ${animaux[0]}    # Affiche: chat
#echo ${animaux[1]}    # Affiche: chien
#echo ${animaux[3]}    # Affiche: oiseau
# Afficher tous le éléments d'un tableau : echo ${animaux[@]}    # Pareil que [*]
# Afficher le nombre des éléments dans le tableau : echo ${#animaux[*]}   # Affiche: 3  nombres des éléments 
# Afficher la langeur de la première élément dans un tableau : echo ${#animaux[0]}
# //// //// //// /// : echo ${#animaux[1]}   # Affiche: 5 (longueur de "chien")

