#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
from collections import OrderedDict

# In[64]:





# In[65]:
# In[66]:

def prepare(code,pheno,study,phenotypep,
            resp):
    dgwas=pd.read_csv(pheno, sep='\t')
    phenotype=pd.read_csv(phenotypep,sep='\t')


# In[67]:


    print('most significant associations')
    print(dgwas.query('~low_confidence_variant').sort_values(['pval'], ascending=[True]).head())


    # In[68]:


    #Use only high confident variant
    dgwas_sub = dgwas.loc[~dgwas['low_confidence_variant'],:]
    snp = pd.DataFrame(dgwas_sub.variant.str.split(':',0).tolist(),columns = ['chr','pos', 'ref', 'alt'])
    dgwas_sub_snp = pd.concat([snp, dgwas_sub.reset_index()], axis=1)


    # In[69]:


    #use snps in chr 1-22
    dgwas_sub_snp_chr = dgwas_sub_snp[dgwas_sub_snp['chr'].isin(list(map(lambda x: str(x), range(1,23))))]


    # In[70]:


    #convert chr/pos type to int
    dgwas_sub_snp_chr.chr = dgwas_sub_snp_chr.chr.astype(int)
    dgwas_sub_snp_chr.pos = dgwas_sub_snp_chr.pos.astype(int)


    # In[71]:


    #use the top 100 associations for fine mapping
    dgwas_min = dgwas_sub_snp_chr.loc[dgwas_sub_snp_chr['pval']<5e-8,:]
    if len(dgwas_min)<100:
        dgwas_min = dgwas_sub_snp_chr.nsmallest(100, 'pval')
    dgwas_min = dgwas_min.sort_values(['chr', 'pos'], ascending=[True, True])


    # In[72]:


    #select interesting regions
    snps = OrderedDict()
    for index, row in dgwas_min.iterrows():
        chrs = row['chr']
        pos = row['pos']
        if chrs in snps:
            if any(list(map(lambda x: x[0] <= pos <= x[1], snps[chrs]))):
                continue
            else:
                snps[chrs].append((pos-1000000, pos+1000000))
        else:
            snps[chrs]= [(int(pos)-1000000, int(pos)+1000000)]
    print("regions to work with:\n", snps)


    # In[73]:


    #get snps in the interesting regions
    n = 1
    for chrs in snps: 
        print("processing chr",chrs)
        for region in snps[chrs]:
            if n == 1:
                table = dgwas_sub_snp_chr.loc[(dgwas_sub_snp_chr["chr"] == chrs) & ( dgwas_sub_snp_chr["pos"] >= region[0]) & 
           (dgwas_sub_snp_chr["pos"] <= region[1]), ]
                table['SEGNUMBER'] = n
            else:
                temp = dgwas_sub_snp_chr.loc[(dgwas_sub_snp_chr["chr"] == chrs) & ( dgwas_sub_snp_chr["pos"] >= region[0]) & 
           (dgwas_sub_snp_chr["pos"] <= region[1]), ]
                temp['SEGNUMBER'] = n
                table = table.append(temp)
        n = n + 1


    # In[74]:


    table['snp'] = table["chr"].map(str) + "_" + table["pos"].map(str)

    #if SNPs have the same position, choose the SNP with the smallest pvalue
    indices = table.groupby('snp')['pval'].idxmin
    table_unique = table.loc[indices]


    # In[75]:


    table_unique = table_unique.sort_values(['chr', 'pos'], ascending=[True, True])


    # In[76]:


    res = table_unique[['variant', 'chr', 'pos', 'tstat', 'minor_AF', 'SEGNUMBER', 'pval']]

    res = res.rename(columns={'variant': 'SNPID', 'chr': 'CHR', 'pos': 'POS',
                       'tstat': 'Z', 'minor_AF': 'F'})


    # In[77]:


    if study == 'cc':
        res['NCONTROL'] = int(phenotype.loc[phenotype['phenotype']==code]['n_controls'])
        res['NCASE'] = int(phenotype.loc[phenotype['phenotype']==code]['n_cases'])
    else:
        res['N'] = int(phenotype.loc[phenotype['phenotype']==code]['n_non_missing'])


    # In[78]:


    res.to_csv(resp,
               sep=' ',header=True, index=False, compression="gzip")

    return res


#only support for both sexes for now
code = 'I10'
pheno = f'/data/analysis/UKBB/raw/{code}.gwas.imputed_v3.both_sexes.tsv'
study = 'cc'
sex='both_sexes'
phenotypep=f'/data/analysis/UKBB/raw/phenotypes.{sex}.tsv.gz'
resp=f'/data/analysis/UKBB/processed/{code}.gwas.imputed_v3.both_sexes.finemapping.tsv.gz'
print(pheno)
prepare(code,pheno,study,phenotypep,
            resp)