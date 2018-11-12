"""UK - biobank snakemake
"""


rule download_ukbb:
    output:
        bgz = "input/UKBB/{phenotype}.gwas.{imputed_version}.{gender}_sexes.tsv.bgz"
    shell:
        "wget ... -o {output.bgz}"  # TODO


rule extract_ukbb:
    input:
        bgz = "input/UKBB/{phenotype}.gwas.{imputed_version}.{gender}.tsv.bgz"
    output:
        tsv = "input/UKBB/{phenotype}.gwas.{imputed_version}.{gender}.tsv"
    shell:
        "zcat {input.bgz} > {output.tsv}"
