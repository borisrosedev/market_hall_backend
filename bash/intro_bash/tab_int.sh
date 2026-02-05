#!/bin/bash
declare -ai nombres=(10 20 30 40 50 )
echo ${nombres[2]}
echo $((nombres[1] + 5))

nombres[3]=$(( nombres[3] + 100))
echo ${nombres[3]} 
