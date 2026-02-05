#!/bin/bash
ligne="Alice:25:Paris:Ingénieur"

# Extraire les champs
nom=${ligne%%:*}
age=${ligne#*:}
age=${age%%:*}
ville=${ligne##*:}
ville=${ville%%:*}

echo "Nom: $nom"      # Alice
echo "Age: $age"      # 25
echo "Ville: $ville"  

