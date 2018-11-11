"""Full workflow for running

[kipoi.models.*.tsv] [annotation.*.tsv] [gwas.tsv]
      \                   |               |
       [merged tsv]

"""

config = {
    "output_dir": 'output'
}

rule merge:
    input:
        kipoi_veff = [],
        anno = []
        gwas = {gwas_txt}
    output:
        os.path.join(config['output_dir'], "merged.tsv")
    shell:
        # TODO
        pass


