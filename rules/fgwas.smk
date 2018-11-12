"""Run fgwas
"""

rule fgwas_run:
    input:
        tsv = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/annotated-variants.tsv.gz"
    output:
        params="output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.params",
        bfs="output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.bfs.gz",
    params:
        study_type = lambda wildcards: config['study_hash'][wildcards.phenotype],
        prefix="output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas",
    shell:
        "my_command -i {input.tsv} -type {params.study_typen} -o {params.prefix}"
        # TODO - fill in


# --------------------------------------------
# compiling the report

def jupyter_nbconvert(input_ipynb):
    subprocess.call(["jupyter",
                     "nbconvert",
                     input_ipynb,
                     "--to", "html"])


def render_ipynb(template_ipynb, rendered_ipynb, params=dict()):
    """Render the ipython notebook
    Args:
      template_ipynb: template ipython notebook where one cell defines the following metadata:
        {"tags": ["parameters"]}
      render_ipynb: output ipython notebook path
      params: parameters used to execute the ipython notebook
    """
    import papermill as pm  # Render the ipython notebook

    os.makedirs(os.path.dirname(rendered_ipynb), exist_ok=True)
    pm.execute_notebook(
        template_ipynb,  # input template
        rendered_ipynb,
        kernel_name="python3",  # default kernel
        parameters=params
    )
    jupyter_nbconvert(rendered_ipynb)


rule fgwas_report:
    """Compile the fgwas report
    """
    input:
        fgwas="output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.bfs.gz",
        tsv = "output/{phenotype}.gwas.{imputed_version}.{gender}/gwas-table-unannotated.tsv.gz"
        ipynb = "src/fgwas_plot.ipynb"
    output:
        ipynb = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/report/fgwas.ipynb",
        html = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/report/fgwas.html",
    run:
        render_ipynb(input.ipynb, output.ipynb,
                     params=dict(fgwas_output=inpu.fgwas,
                                 gwas=input.tsv,
                                 chrs=wildcards.chr))
        jupyter_nbconvert(output.ipynb)
