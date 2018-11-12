"""UK - biobank snakemake
"""
import pandas as pd
from kipoi_gwas.prepare import prepare

def get_url(fname):
    df = pd.read_table("metadata/UKBB-GWAS-Imputed-v3201807.tsv.gz")
    return df[df.File.str.contains(fname)]['Dropbox File'].iloc[0]


rule download_ukbb:
    output:
        bgz = "input/UKBB/{file}.tsv.bgz"
    params:
        url = lambda wildcards: get_url(wildcards.file)
    shell:
        "wget {params.url} -O {output.bgz}"


rule extract_ukbb:
    input:
        bgz = "input/UKBB/{file}.tsv.bgz"
    output:
        tsv = "input/UKBB/{file}.tsv"
    shell:
        "zcat {input.bgz} > {output.tsv}"


rule prepare_merge_table:
    input:
        phenotype_tsv = "input/UKBB/phenotypes.{gender}.tsv",
        tsv = "input/UKBB/{phenotype}.gwas.{imputed_version}.{gender}.tsv"
    output:
        tsv = "output/{phenotype}.gwas.{imputed_version}.{gender}/gwas-table-unannotated.tsv.gz"
    run:
        study = config['study_hash'][wildcards.phenotype]
        prepare(wildcards.phenotype, input.tsv, study, input.phenotype_tsv, output.tsv)

#only support for both sexes for now
