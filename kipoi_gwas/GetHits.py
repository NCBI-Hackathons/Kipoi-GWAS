#!/usr/bin/env python
# coding: utf-8

# In[190]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
from glob import glob
from collections import OrderedDict

ddir = "data"

dgwas=pd.read_csv(f'{ddir}/UKBB/raw/I10.gwas.imputed_v3.both_sexes.tsv',sep='\t')
phenotype=pd.read_csv(f'{ddir}/UKBB/raw/phenotypes.both_sexes.tsv.gz',sep='\t')


# In[202]:


#Use only high confident variant
dgwas_sub = dgwas.loc[~dgwas['low_confidence_variant'],:]
snp = pd.DataFrame(dgwas_sub.variant.str.split(':',0).tolist(),columns = ['chr','pos', 'ref', 'alt'])
dgwas_sub_snp = pd.concat([snp, dgwas_sub.reset_index()], axis=1)


# In[203]:


#use snps in chr 1-22
dgwas_sub_snp_chr = dgwas_sub_snp[dgwas_sub_snp['chr'].isin(list(map(lambda x: str(x), range(1,23))))]


# In[204]:


print(dgwas_sub_snp_chr['chr'].unique())
print(dgwas_sub_snp_chr.head())
dgwas_sub_snp_chr.chr = dgwas_sub_snp_chr.chr.astype(int)
dgwas_sub_snp_chr.pos = dgwas_sub_snp_chr.pos.astype(int)


# In[206]:


dgwas_min = dgwas_sub_snp_chr.nsmallest(100, 'pval')
dgwas_min = dgwas_min.sort_values(['chr', 'pos'], ascending=[True, True])


# In[209]:


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


# In[292]:


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


# In[293]:


table['snp'] = table["chr"].map(str) + "_" + table["pos"].map(str)
print(table.shape)


# In[301]:


indices = table.groupby('snp')['pval'].idxmin
table_unique = table.loc[indices]


# In[319]:


table_unique = table_unique.sort_values(['chr', 'pos'], ascending=[True, True])
table_unique.head()


# In[320]:


res = table_unique[['variant', 'chr', 'pos', 'tstat', 'minor_AF', 'SEGNUMBER']]


# In[321]:


res = res.rename(columns={'variant': 'SNPID', 'chr': 'CHR', 'pos': 'POS',
                   'tstat': 'Z', 'minor_AF': 'F'})


# In[322]:


res['NCONTROL'] = int(phenotype.loc[phenotype['phenotype']=='I10']['n_controls'])
res['NCASE'] = int(phenotype.loc[phenotype['phenotype']=='I10']['n_cases'])


# In[323]:


res.to_csv('/data/analysis/UKBB/processed/I10.gwas.imputed_v3.both_sexes.finemapping.tsv.gz',
           sep=' ',header=True, index=False, compression="gzip")
           


# In[324]:


res['pheno'] = np.around(np.random.uniform(0,1,res.shape[0]), decimals=3)


# In[325]:


res.to_csv('/data/analysis/UKBB/processed/I10.gwas.imputed_v3.both_sexes.finemapping.pheno.tsv.gz',
           sep=' ',header=True, index=False, compression="gzip")

