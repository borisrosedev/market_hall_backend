#!/bin/bash
chemin="/home/user/documents/file.txt"
#extraire le file.txt
nom=${chemin##*/}
echo "Nom: $nom " 

#extraire le document
parent=${chemin%/*}
parent=${parent##*/}

echo "Prent: $parent"
