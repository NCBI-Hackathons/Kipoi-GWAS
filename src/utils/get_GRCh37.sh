#! /usr/bin/env bash
host="ftp://ftp.ensembl.org"
loc="/pub/grch37/update/fasta/homo_sapiens/dna/"
root="Homo_sapiens.GRCh37.dna.chromosome"
ext="fa.gz"
out=$1
mkdir -p $out
k=($(seq  22) X Y)

for i in ${k[@]}; do
	fn=${root}.$i.${ext}
	target=${host}${loc}${fn}
	echo getting $target
	wget $target -O ${out}/${fn}
done

cd $out
gunzip *.${ext}
sed  -e 's/^>/>chr/' *.fa

