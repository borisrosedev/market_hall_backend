#!/bin/bash

animaux=("cheval" "vache" "anne" )

for animal in ${animaux[*]}
do 
	echo "Animal $animal"
done 

# Boucler les indexs 
for i in ${animaux[*]}
do 
	echo "[$i] = ${animaux[i]}"
done 
