#!/usr/bin/env bash

orig=$1

cols=$(head -n 1 $1 |sed 's/\s/\n/g' |grep -n diff |cut -f 1 -d ':'|tr "\n" "," | sed 's/,$//')
cut -f 1,$cols $1
