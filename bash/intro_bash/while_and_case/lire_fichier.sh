#!/bin/bash

# Créer un fichier test
cat > users.txt << EOF
Alice
Bob
Charlie
EOF

# Lire le fichier ligne par ligne
while read nom
do
    echo "Utilisateur: $nom"
done < users.txt

rm users.txt
