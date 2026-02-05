#!/bin/bash
#les éléments de tableau avec des indexes précis 
declare -a notes=([0]="Yaya" [2]="mahmoud" [6]="alhot")

declare -a animaux=( "chat" "chien" "souris" "oiseau" )

echo "Lists des élélments dans le tableau: ${animaux[@]}"

echo "Affichage des éléments avec des indexs "
echo "L'index 0 : ${notes[0]}"
echo "L'index 2 : ${notes[2]}"
echo "L'index 6 : ${notes[6]}"

for animal in ${animeaux[@]} 
do 
	echo "Animal : $animal"
done 
