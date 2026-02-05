#!/bin/bash

read -p "Entrez quelque chose: " input

case $input in 
	[0-9]*) echo "Commence par un chiffre";;
	[a-z]*) echo "Commence par un lettre minuscule";;
	[A-Z]*) echo "Commence par une lettre majuscule";;
	*) echo "Autre caractère";; 
esac 
