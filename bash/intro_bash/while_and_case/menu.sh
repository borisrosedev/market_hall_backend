#!/bin/bash

echo "=== Menu ==="
echo "1) Lister les fichiers"
echo "2) Créer un dossier"
echo "3) Quitter"
read -p "Choix: " choix

case $choix in
    1) ls ;;
    2) read -p "Nom: " nom; mkdir "$nom" ;;
    3) echo "Au revoir!"; exit 0 ;;
    *) echo "Choix invalide" ;;
esac
