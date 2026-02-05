#!/bin/bash
email="yaya@example.com"
#extraire le domaine
domaine=${email#*@}
echo "Domaine: $domaine"

#extraire le nom 
nom=${email%@*}
echo "Nom : $nom" 

