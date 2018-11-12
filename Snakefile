"""Full workflow for running

[kipoi.models.*.tsv] [annotation.*.tsv] [gwas.tsv]
      \                   |               |
       [merged tsv]

"""
import glob
from kipoi_gwas import regulatory_features

config = {
    "output_dir": 'output'
}

#-----------pipeline----------------
rule step01_get_phenotype_from_ukbb:
    input:
    output:
    shell:

rule step02_download:
    input:
    output:
    shell:

rule step03_merge:
    input:
    output:
    shell:

rule step04_fgwas:
    input:
    output:
    shell:

        #---------------------------------


rule fetch_regulatry_features:
    output:
        '{fdir}/bar_dgff_regulation_combo_type.png'
    run:
        regulatory_features.run(wildcards.ddir)


# --------------------------------------------

include:
    "rules/merge/deepsea.smk"
include:
    "rules/merge/deepbind.smk"
include:
    "rules/fgwas.smk"
include:
    "rules/ukbb.smk"
