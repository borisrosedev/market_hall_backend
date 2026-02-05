#!/bin/bash
if [[ $# -eq 0 ]]
then 
	echo "Aucune argument"
	exit 1 
fi 

if [[ ! -f $1 ]] 
then 
	echo "Le fichier $1 n'existe pas " 
	exit 1
fi 

echo "Le fichier trouvé: $1 " 
