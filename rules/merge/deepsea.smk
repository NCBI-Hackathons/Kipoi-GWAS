"""Join the snakemake for DeepSEA
"""

rule merge_deepsea:
    input:
        tsv = "input/anno/kipoi/subset/{chr}/DeepSEA.tsv"
        ukbb_tsv = "input/UKBB/{phenotype}.gwas.imputed_v3.both_sexes.tsv"
    output:
        tsv = "output/{phenotype}/subset/{chr}/DeepBind/fgwas/input/annotated-variants.tsv.gz"
    shell:
        "TODO"
