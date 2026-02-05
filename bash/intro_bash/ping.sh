#!/bin/bash
function ping
{
echo pign
if (( i > 0))
then
((i--))
echo pong
fi
}

function pong
{
echo pong
if (( i > 0 ))
then
 ((i--))
ping
fi
}
declare -i i=4
ping
