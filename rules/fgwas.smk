"""Run fgwas
"""

rule fgwas_prepare_tables:
    input:
        tsv = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/annotated-variants.tsv.gz"
    output:
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.params",
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.llk",
    shell:
        "-o output/{wildcards.phenotype}/subset/{wildcards.chr}/{wildcards.run_id}/fgwas/input/fgwas"
        # TODO


rule fgwas_run:
    input:
        tsv = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/annotated-variants.tsv.gz"
    output:
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.params",
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.llk",
    shell:
        "-o output/{wildcards.phenotype}.gwas.{imputed_version}.{gender}/subset/{wildcards.chr}/{wildcards.run_id}/fgwas/input/fgwas"
        # TODO


rule fgwas_report:
    input:
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.params",
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.llk",
    output:
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.llk",
    run:
        pass

# TODO - compile the reports
