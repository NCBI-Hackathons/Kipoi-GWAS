"""UK - biobank snakemake
"""
import pandas as pd
def get_url(fname):
    df = pd.read_table("metadata/UKBB-GWAS-Imputed-v3201807.tsv.gz")
    return df[df.File == fname]['Dropbox File'].iloc[0]


rule download_ukbb:
    output:
        bgz = "input/UKBB/{file}.tsv.bgz"
    params:
        url = lambda wildcards: get_url(wildcards.file)
    shell:
        "wget {params.url} -O {output.bgz}"


rule extract_ukbb:
    input:
        bgz = "input/UKBB/{phenotype}.gwas.{imputed_version}.{gender}.tsv.bgz"
    output:
        tsv = "input/UKBB/{phenotype}.gwas.{imputed_version}.{gender}.tsv"
    shell:
        "zcat {input.bgz} > {output.tsv}"
