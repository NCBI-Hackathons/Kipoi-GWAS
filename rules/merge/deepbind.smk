# TODO - get the deepbind wildcard


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
        ukbb = "input/UKBB/{phenotype}.gwas.imputed_v3.both_sexes.tsv"
        deepbind_files = glob.glob("input/anno/kipoi/subset/{chr}/DeepBind/*.tsv.gz")
    output:
        tsv = "output/{phenotype}/subset/{chr}/DeepBind/fgwas/input/annotated-variants.tsv.gz"
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
