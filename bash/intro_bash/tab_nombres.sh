#!/bin/bash

declare -a notes=( 15 18 12 15 16 )

# Affiche les notes
echo "Notes: ${notes[*]}"

# Somme des notes
somme=0
for note in ${notes[*]}
do
    somme=$(( somme + note ))
done

moyenne=$(( somme / ${#notes[*]} ))
echo "Moyenne: $moyenne"
