#!/bin/bash

read -p "Entrez o ou O: " rep

case $rep in
    o|O)  echo "OUI" ;;
    *)    echo "Autre réponse" ;;
esac
