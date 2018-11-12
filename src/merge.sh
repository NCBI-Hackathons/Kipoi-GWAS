#!/usr/bin/env bash
assocf=$1 #GWAS phenotype association
annotf=$2 #Annotation file
chrom=$3 #Chromosome
filter_str=$4 #straing to filter annotation columns
outf=$5 #Output file

tmpd=/tmp/$(date +%s).$$
echo Intermediate results will be stored in ${tmpd}
mkdir ${tmpd}
assocfn=${assocf%.*}
annotfn=${annotf%.*}

# Filter input model columns
if [ ! -z $(echo "${filter_str}"|sed 's/\s+//') ]; then
	echo Filtering input
	cols=$(head -n 1 "${annotf}" |sed 's/\s/\n/g' |grep -n "${filter_str}" |cut -f 1 -d ':'|tr "\n" "," | sed 's/,$//')
	cut -f 1,$cols "${annotf}" >"${tmpd}"/tmp_annotf_filtered.tmp
else
	echo Filtering skipped
	cp "${annotf}" "${tmpd}"/tmp_annotf_filtered.tmp
fi

# Extract ids of the variants in the association set and filter by chromosome, no missing or indels (res: pheno_ids)
cut -f 1 -d ' ' "${assocf}" |grep ^${chrom} | awk 'BEGIN{FS=":"; OFS="";} {if(length($3) == 1 && length($4) ==1 && $4!="\.") print $1,":",$2,":",$3,":[",$4,"]"}'>${tmpd}/ids_assocf.${chrom}.tmp
assochead=$(head -n 1 "${assocf}") 
grep -f ${tmpd}/ids_assocf.${chrom}.tmp "${assocf}" >${tmpd}/tmp_assocf.${chrom}.tmp

# Subset the model file to the pheno_ids
cut -f 1 -d ' ' "${assocf}" |grep ^${chrom} | awk 'BEGIN{FS=":"; OFS="";} {if(length($3) == 1 && length($4) ==1 && $4!="\.") print "chr",$1,":",$2,":",$3,":[\47",$4,"\47]"}'>${tmpd}/ids_annotf.${chrom}.tmp
annothead=$(head -n 1 "${tmpd}"/tmp_annotf_filtered.tmp)
grep -F -f ${tmpd}/ids_annotf.${chrom}.tmp "${tmpd}"/tmp_annotf_filtered.tmp |cut -f 1 --complement |sed 's/\t/ /g' >${tmpd}/tmp_annotf.${chrom}.tmp

# Append models to assciation file
echo ${assochead} $(echo ${annothead} |cut -f1 -d ' ' --complement| sed 's/\t/ /g') >${outf}
paste -d ' ' ${tmpd}/tmp_assocf.${chrom}.tmp ${tmpd}/tmp_annotf.${chrom}.tmp >>${outf}

# Cleaning up
echo Cleaning up
rm ${tmpd}/*
rmdir ${tmpd}
echo Done
