#!/bin/bash
while true 
do 
	echo "=== Menu ==="
	echo "1) Lister les fichieres " 
	echo "2) Créer un dossier "
	echo "3) Quiter "
	read -p "Choix: " choix 

if [[ $choix == 1 ]]
then 
	ls 
elif [[ $choix == 2 ]]
then 
	read -p "Nom du dossier: " nom
	mkdir "$nom"
	echo "Le dossier nomé " $nom " bien été créé" 
elif [[ $choix == 3 ]]
then 
	echo "Down " 
	exit 0 
else 
	echo "Choix invalide " 
fi 
done 
