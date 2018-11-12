"""Join the snakemake for DeepSEA
"""

rule merge_deepsea:
    input:
        tsv = "input/anno/kipoi/subset/{chr}/DeepSEA.tsv",
        ukbb_tsv = "input/UKBB/{phenotype}.gwas.{imputed_version}.{gender}.tsv"
    output:
        tsv = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/DeepBind/fgwas/input/annotated-variants.tsv.gz"
    shell:
        "TODO"
