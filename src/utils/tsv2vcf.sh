#! /usr/bin/env bash

intsv=$1
outvcf=$2
head=$3

#get the vcf fields
#add 'chr'
#remove indels
awk 'BEGIN{OFS="";} NR>1 {if(length($4) == 1 && length($5) ==1 && $5!="\.") print "chr",$2,"\t",$3,"\t",$7,"\t",$4,"\t",$5,"\t.\tPASS\t."}' "${intsv}" >/tmp/${intsv}.nohead

#add the header
cat ${head} /tmp/${intsv}.nohead


