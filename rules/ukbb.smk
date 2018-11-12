"""UK - biobank snakemake
"""


rule download_ukbb:
    output:
        bgz = "input/UKBB/{phenotype}.gwas.imputed_v3.both_sexes.tsv.bgz"
    shell:
        "wget ... -o {output.bgz}"  # TODO


rule extract_ukbb:
    input:
        bgz = "input/UKBB/{phenotype}.gwas.imputed_v3.both_sexes.tsv.bgz"
    output:
        tsv = "input/UKBB/{phenotype}.gwas.imputed_v3.both_sexes.tsv"
    shell:
        "zcat {input.bgz} > {output.tsv}"
