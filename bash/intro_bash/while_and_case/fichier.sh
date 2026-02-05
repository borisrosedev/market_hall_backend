#!/bin/bash

fichier=$1

case $fichier in
    *.txt) echo "Fichier texte" ;;
    *.pdf) echo "Fichier PDF" ;;
    *.mp3) echo "Fichier audio" ;;
    *.jpg|*.png) echo "Image" ;;
    *) echo "Type de fichier non valide" ;;
esac
