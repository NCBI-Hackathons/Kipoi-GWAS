"""Run fgwas
"""


rule run_fwgwas:
    input:
        tsv = "output/{phenotype}/subset/{chr}/{run_id}/fgwas/input/annotated-variants.tsv.gz"
    output:
        tsv = "output/{phenotype}/subset/{chr}/{run_id}/fgwas/input/fgwas.params"
    shell:
        "-o output/{wildcards.phenotype}/subset/{wildcards.chr}/{wildcards.run_id}/fgwas/input/fgwas.params"
        # TODO


# TODO - compile the reports
