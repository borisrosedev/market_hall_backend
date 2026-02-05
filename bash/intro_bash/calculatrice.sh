#!/bin/bash
# calculatrice.sh - Mini-calculatrice en bash

echo "=== Mini-calculatrice ==="
echo ""

# Définir deux nombres
nombre1=15
nombre2=4

echo "Nombre 1 : $nombre1"
echo "Nombre 2 : $nombre2"
echo ""

# Tous les calculs
echo "Addition       : $nombre1 + $nombre2 = $((nombre1 + nombre2))"
echo "Soustraction   : $nombre1 - $nombre2 = $((nombre1 - nombre2))"
echo "Multiplication : $nombre1 * $nombre2 = $((nombre1 * nombre2))"
echo "Division       : $nombre1 / $nombre2 = $((nombre1 / nombre2))"
echo "Modulo         : $nombre1 % $nombre2 = $((nombre1 % nombre2))"
echo "Puissance      : $nombre1 ^ $nombre2 = $((nombre1 ** nombre2))"
