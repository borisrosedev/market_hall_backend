#!/bin/bash

case $# in 
	0) echo "Aucun argument";;
	1) echo "1 argument: $1";;
	2) echo "2 arguments : $1 et $2";;
	*) echo "Plus de 2 arguments ";; 
esac 
