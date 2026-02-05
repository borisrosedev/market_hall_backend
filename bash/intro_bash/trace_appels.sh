#!/bin/bash
function f2
{
echo " ------ Dans f2 :"
echo " ------ FUNCNAME : $FUNCNAME"
echo " ------ tableau FUNCNAME[] : ${FUNCNAME[*]}"
}function f1
{
echo " --- Dans f1 :"
echo " --- FUNCNAME : $FUNCNAME"
echo " --- tableau FUNCNAME[] : ${FUNCNAME[*]}"
echo " --- - Appel a f2 "
echo
f2
}
echo "Debut :"
echo "FUNCNAME : $FUNCNAME"
echo "tableau FUNCNAME[] : ${FUNCNAME[*]}"
echo

