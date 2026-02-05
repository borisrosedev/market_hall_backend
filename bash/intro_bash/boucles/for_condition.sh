#!/bin/bash

for fichier in $(ls)
do 
	if [[ -f $fichier ]]
	then 
		echo "Fichier : $fichier" 
	elif [[ -d $fichier ]] 
	then 
		echo "Dosseir : $fichier " 
	fi
done 
