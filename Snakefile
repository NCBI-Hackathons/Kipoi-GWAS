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
def read_tsv(fname, col_selector):
    """Load the Kipoi output tsv and set SNPID as index

    Args:
      fname: file name of a .tsv or .tsv.gz file
      col_selector: columns wildcard. Example: '.*diff.*'

    Returns:
      pandas data-frame with SNPID index
    """
    df = pd.read_table(fname)
    df['SNPID'] = (df['variant_chr'].str.replace("chr", "") + ":" +
                   df['variant_pos'].astype(str) + ":" +
                   df['variant_ref'] + ":" + df['variant_alt'])
    df = df.set_index('SNPID')

    # TODO - write a Dask version for it
    return df.iloc[:, df.columns.str.match(col_selector)]


rule merge_deepbind:
    """Load all the DeepBind files and merge them with the UKBB table
    """
    input:
        ukbb = "I10.gwas.imputed_v3.both_sexes.finemapping.tsv.gz",
        deepbind_files = glob.glob("DeepBind/*.tsv.gz")
    output:
        tsv = "DeepBind/merged.tsv.gz"
    run:
        # UK BB table
        dfbb = pd.read_table(input.ukbb, sep=' ')

        # Load all the Kipoi tables
        df = pd.concat([read_tsv(f, '.*diff.*').
                        rename(columns={"preds/diff/0": f.replace("tsv.gz", "")})
                        for f in input.deepbind_files], axis=1)

        # Merge the two tablesdd
        dfo = pd.merge(dfbb, df, left_index=True, right_index=True)

        # Write the results to as tsv table
        dfo = dfo.reset_index()
        dfo.to_csv(output.tsv, compression='gzip', sep=' ', index=False)

rule fetch_regulatry_features:    
    output: 
        '{fdir}/bar_dgff_regulation_combo_type.png'
    run:
        regulatory_features.run(wildcards.ddir)

rule merge:
    input:
        kipoi_veff = [],
        anno = []
        gwas = {gwas_txt}
    output:
        os.path.join(config['output_dir'], "merged.tsv")
    shell:
        # TODO(Ziga) - use dask to join the tables
        pass

