#!/usr/bin/env bash
assocf=$1
annotf=$2
chrom=$3
outf=$4

tmpd=/tmp/$(date +%s).$$
echo Intermediate results will be stored in ${tmpd}
mkdir ${tmpd}
assocfn=${assocf%.*}
annotfn=${annotf%.*}

# Extract ids of the variants in the association set and filter by chromosome, no missing or indels (res: pheno_ids)
cut -f 1 -d ' ' "${assocf}" |grep ^${chrom} | awk 'BEGIN{FS=":"; OFS="";} {if(length($3) == 1 && length($4) ==1 && $4!="\.") print $1,":",$2,":",$3,":[",$4,"]"}'>${tmpd}/ids_assocf.${chrom}.tmp
assochead=$(head -n 1 "${assocf}") 
grep -f ${tmpd}/ids_assocf.${chrom}.tmp "${assocf}" >${tmpd}/tmp_assocf.${chrom}.tmp

# Subset the model file to the pheno_ids
cut -f 1 -d ' ' "${assocf}" |grep ^${chrom} | awk 'BEGIN{FS=":"; OFS="";} {if(length($3) == 1 && length($4) ==1 && $4!="\.") print "chr",$1,":",$2,":",$3,":[\47",$4,"\47]"}'>${tmpd}/ids_annotf.${chrom}.tmp
annothead=$(head -n 1 "${annotf}")
grep -F -f ${tmpd}/ids_annotf.${chrom}.tmp "${annotf}"|cut -f 1 --complement |sed 's/\t/ /g' >${tmpd}/tmp_annotf.${chrom}.tmp

# Append models to assciation file
echo ${assochead} $(echo ${annothead} |cut -f1 -d ' ' --complement| sed 's/\t/ /g') >${outf}
paste -d ' ' ${tmpd}/tmp_assocf.${chrom}.tmp ${tmpd}/tmp_annotf.${chrom}.tmp >>${outf}

# Cleaning up
echo Cleaning up
rm ${tmpd}/*
rmdir ${tmpd}
echo Done
