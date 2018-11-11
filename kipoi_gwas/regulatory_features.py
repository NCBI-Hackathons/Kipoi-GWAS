#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('bash', '', 'tree data')


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from glob import glob


# In[3]:


ddir = "data"


# In[4]:


# release 75
# dAnnotatedFeatures=pd.read_csv(f'{ddir}/ensembl/raw/ftp.ensembl.org/pub/release-75/regulation/homo_sapiens/AnnotatedFeatures.gff.gz',
#                                names=['chromosome', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'],
#                                 sep='\t')


# ## GWAS table flitering

# In[5]:


dgwas_subset=pd.read_csv('/data/analysis/UKBB/raw/I10.gwas.imputed_v3.both_sexes.chr12.tsv',sep='\t',)
# dgwas=pd.read_csv('/data/analysis/UKBB/raw/variants.tsv',sep='\t')


# In[6]:


print(dgwas_subset.shape)


# In[9]:


# dgwas_subset_flt=dgwas_subset.loc[~dgwas_subset['low_confidence_variant'],:]
# print(dgwas_subset_flt.shape)


# In[114]:


# dgwas_subset.loc[]
_=dgwas_subset_flt['pval'].apply(np.log10).hist()


# In[115]:


sum(dgwas_subset_flt['pval']<1e-02)


# In[116]:


dgwas_subset['pval'].min()


# In[117]:


dgwas_subset.head()


# In[118]:


dgwas_subset_flt.shape


# In[119]:


dgwas_subset_flt.to_csv('/data/analysis/UKBB/processed/dgwas_subset_flt.tsv',sep='\t',)


# In[121]:


dgwas_subset_flt.to_parquet('/data/analysis/UKBB/processed/dgwas_subset_flt.pqt',compression='gzip',
                           engine='fastparquet')


# In[ ]:





# ## Combining regulatory features

# In[46]:


import glob
from os.path import exists,dirname,basename


# In[54]:


i=0
for gffp in glob.iglob(f'{ddir}/ensembl/raw/ftp.ensembl.org/pub/grch37/update/regulation/homo_sapiens/RegulatoryFeatureActivity/*/homo_sapiens*.gff.gz'):
    dgff_regulation=pd.read_table(f'{ddir}/ensembl/raw/ftp.ensembl.org/pub/grch37/update/regulation/homo_sapiens/RegulatoryFeatureActivity/A549/homo_sapiens.GRCh37.A549.Regulatory_Build.regulatory_activity.20161117.gff.gz',
                             names=['chromosome', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'])
    dgff_regulation['tissue type']=basename(dirname(gffp))
    if i==0:
        dgff_regulation_combo=dgff_regulation.copy()
    else:
        dgff_regulation_combo=dgff_regulation_combo.append(dgff_regulation)
    del dgff_regulation
    print(dgff_regulation_combo.shape)
    i+=1
#     break


# In[84]:


dgff_regulation_combo.head()


# In[83]:


840081-1120108


# In[95]:


import matplotlib.pyplot as plt
# plt.style.use('ggplot')
import seaborn as sns
sns.set('notebook')


# In[97]:


get_ipython().run_line_magic('mkdir', 'plot')


# In[100]:


ax=dgff_regulation_combo['type'].value_counts().plot.barh()
plt.savefig('plot/bar_dgff_regulation_combo_type.svg')
plt.savefig('plot/bar_dgff_regulation_combo_type.png')
plt.tight_layout()


# In[ ]:





# In[102]:


len(dgff_regulation_combo['regulatory_feature_stable_id'].unique())


# In[101]:


dgff_regulation_combo.head()


# In[106]:


dgff_regulation_combo.loc[(dgff_regulation_combo['regulatory_feature_stable_id']=='ENSR00000408425'),:].shape


# In[108]:


len(dgff_regulation_combo['tissue type'].unique())


# In[ ]:





# In[ ]:





# In[ ]:





# In[55]:


dgff_regulation_combo['regulatory_feature_stable_id']=dgff_regulation_combo['attributes'].apply(lambda x : [s.replace('regulatory_feature_stable_id=','') for s in x.split(';') if 'regulatory_feature_stable_id=' in s][0])


# In[61]:


# dgff_regulation_combo.to_csv(f'{ddir}/ensembl/raw/dgff_regulation_combo.tsv',sep='\t')


# In[62]:


f'{ddir}/ensembl/raw/dgff_regulation_combo.tsv'


# In[63]:


get_ipython().run_line_magic('ls', '-ltr data/ensembl/raw/dgff_regulation_combo.tsv')


# In[75]:


# to_table_pqt(dgff_regulation_combo.head(),'test.pqt')
#f'{ddir}/ensembl/raw/dgff_regulation_combo.pqt'
dgff_regulation_combo.loc[:,['chromosome',
 'source',
 'type',
 'start',
 'end',
 'score',
 'strand',
 'phase',
#  'attributes',
 'tissue type',
 'regulatory_feature_stable_id']].to_parquet('dgff_regulation_combo.pqt',engine='fastparquet',compression='gzip',)


# In[77]:


dgff_regulation_combo["type"].value_counts()


# In[80]:


dgff_regulation_combo["end"].max()


# In[ ]:





# In[ ]:





# In[79]:





# ## read

# In[10]:


dgff_regulation_combo=pd.read_parquet(f'{ddir}/ensembl/processed/dgff_regulation_combo.pqt',engine='fastparquet')


# In[13]:


dgff_regulation_combo_subset=dgff_regulation_combo.loc[((dgff_regulation_combo["tissue type"]=='Aorta') & (dgff_regulation_combo["chromosome"]=='12')),:]


# In[ ]:


dgff_regulation_combo_subset


# In[129]:


dgff_regulation_combo['chromosome'].unique()


# In[134]:


print(dgff_regulation_combo_tissue.shape)


# In[ ]:





# In[132]:


dgff_regulation_combo_tissue.head()


# In[ ]:


df=dgwas_subset_flt['variant'].apply(lambda x : x.split(':')).apply(pd.Series)


# In[ ]:


dgwas_subset_flt=dgwas_subset_flt.join(df)


# In[122]:


dgwas_subset_flt.head()


# In[ ]:





# In[ ]:





# In[ ]:


# save gwas variants as bed %%file


# In[131]:


bed_colns = ['chromosome','start','end','id','NM','strand']


# In[78]:


dgff_regulation_combo_tissue.loc[:,['chromosome','start','end','regulatory_feature_stable_id','NM','strand']].to_csv(f'{ddir}/ensembl/processed/dgff_regulation_combo_tissue.bed',
                                                                                                                     index=False,
                                                                                                                     header=False,sep='\t')


# In[ ]:


# dgff_regulation_combo.loc[:,"att"]


# In[51]:


# trying to collapse the tissue wise regulation features
# cols_dgff_regulation_combo=dgff_regulation_combo.columns.tolist()

# for ch in dgff_regulation_combo['chromosome'].unique():
#     for ft in dgff_regulation_combo['type'].unique():
#         dgff_regulation_combo_ch=dgff_regulation_combo.loc[((dgff_regulation_combo['chromosome']==ch) & (dgff_regulation_combo['type']==ft)),:]
#         dgff_regulation_combo_ch=dgff_regulation_combo_ch.reset_index()
#         break
#     break

# print(dgff_regulation_combo_ch.shape)

# # dgff_regulation_combo_summed=pd.DataFrame(columns=[ft],
# # #                                           index=[1,2]
# # index=range(dgff_regulation_combo_ch['start'].min(),dgff_regulation_combo_ch['end'].max()+1),
# #                                          )
# # dgff_regulation_combo_summed[ft]=0
# # dgff_regulation_combo_summed['chromosome']=ch
# # print(dgff_regulation_combo_summed.shape)

# for idx in dgff_regulation_combo_ch.index:
#     start,end= dgff_regulation_combo_ch.loc[idx,'start'],dgff_regulation_combo_ch.loc[idx,'end']
#     dgff_regulation_combo_summed.loc[start:end,ft]=dgff_regulation_combo_summed.loc[start:end,ft]+1
# #     break

# dgff_regulation_combo_summed.loc[start:end,ft]


# In[58]:


dgff_regulation_combo_summed.head()


# In[ ]:


dgff_regulation_combo_summed.TF_binding_site.value_counts()


# In[59]:


dgff_regulation_combo_summed.shape


# In[ ]:


TF_binding_site


# In[54]:


dgff_regulation_combo_ch.head()


# In[ ]:





# In[ ]:





# In[48]:


end


# In[ ]:





# In[39]:


dgff_regulation_combo_ch.head().loc[:,['start','end']].to_tuples()()


# In[30]:


dgff_regulation_combo_summed.shape


# In[31]:


dgff_regulation_combo_ch.head()


# In[ ]:





# In[ ]:





# In[27]:


dgff_regulation_combo_summed


# In[16]:


list(range(1,5))


# In[ ]:





# In[8]:


# dpeaksgff=pd.read_table(f'{ddir}/ensembl/raw/ftp.ensembl.org/pub/grch37/update/regulation/homo_sapiens/Peaks/A549/CTCF/homo_sapiens.GRCh37.A549.CTCF.SWEmbl_R0005_IDR.peaks.20161117.gff.gz')


# In[65]:


dgff_regulation_combo.head()


# In[66]:


dgff_regulation_combo.columns.tolist()


# In[ ]:





# In[ ]:





# In[ ]:





# In[11]:


dgff_regulation.head()


# In[42]:


dgff_regulation.shape


# In[44]:


dgff_regulation["type"].value_counts()


# In[ ]:





# In[ ]:





# In[ ]:




