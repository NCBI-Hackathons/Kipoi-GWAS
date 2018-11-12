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
        # TODO - run the script


rule fgwas_run:
    input:
        tsv = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/annotated-variants.tsv.gz"
    output:
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.params",
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.llk",
    shell:
        "-o output/{wildcards.phenotype}.gwas.{imputed_version}.{gender}/subset/{wildcards.chr}/{wildcards.run_id}/fgwas/input/fgwas"
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
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.params",
        "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/input/fgwas.llk",
        ipynb = "src/notebook.ipynb"
    output:
        ipynb = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/report/fgwas.ipynb",
        html = "output/{phenotype}.gwas.{imputed_version}.{gender}/subset/{chr}/{run_id}/fgwas/report/fgwas.html",
    run:
        # TODO - parametrize the notebook
        render_ipynb(input.ipynb, output.ipynb, params=dict())
        jupyter_nbconvert(output.ipynb)
