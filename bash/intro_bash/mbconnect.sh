#!/bin/bash 
echo "L'utilisateur est : $(who | wc -l) "
echo "Le uptime est : $(uptime)" 
echo "Les utilisateurs : $(users) " 
echo " $(who -q)" 
