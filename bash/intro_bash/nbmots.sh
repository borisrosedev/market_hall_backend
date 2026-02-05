#!/bin/bash
echo "Entrez une suite de mots : " 
#tableau pour stocker les mots siasi pra l'utilisateur 
read -a mots

#compter le nombre des mots 
nombre=${#mots[@]} 
echo "$nombre mots ont été saisi "
