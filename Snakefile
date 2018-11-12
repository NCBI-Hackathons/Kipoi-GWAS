"""Full workflow for running

[kipoi.models.*.tsv] [annotation.*.tsv] [gwas.tsv]
      \                   |               |
       [merged tsv]

"""
import glob

# config = {
#     "output_dir": 'output'
# }

# --------------------------------------------
# All the runs
run_ids = ['DeepSEA', 'DeepBind']
chrs = ['chr12']
phenotypes = ['I10']
imputed_version = ['imputed_v3']
gender = ['both_sexes']
#-----------pipeline----------------
rule all:
    input:
        expand("output/{phenotype}.gwas.{imputed_version}.{gender}"
               "/subset/{chr}/{run_id}/fgwas/input/fgwas.llk",
               chr=chrs,
               imputed_version=imputed_version,
               gender=genders,
               run_id=run_ids,
               phenotype=phenotypes),
        expand("output/{phenotype}.gwas.{imputed_version}.{gender}"
               "/subset/{chr}/{run_id}/fgwas/report/fgwas.html",
               chr=chrs,
               run_id=run_ids,
               imputed_version=imputed_version,
               gender=gender,
               phenotype=phenotypes)

# --------------------------------------------

include:
    "rules/merge/deepsea.smk"
include:
    "rules/merge/deepbind.smk"
include:
    "rules/fgwas.smk"
include:
    "rules/ukbb.smk"
include:
    "rules/ensembl.smk"
