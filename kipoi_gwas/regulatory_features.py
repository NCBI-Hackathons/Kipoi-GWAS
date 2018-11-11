#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
from glob import glob
import glob
from os.path import exists,dirname,basename
import matplotlib.pyplot as plt
# plt.style.use('ggplot')
import seaborn as sns
sns.set('notebook')

# global vars of package
# from kipoi_gwas import ddir
ddir = "data"
fdir = "figure"

# release 75
# dAnnotatedFeatures=pd.read_csv(f'{ddir}/ensembl/raw/ftp.ensembl.org/pub/release-75/regulation/homo_sapiens/AnnotatedFeatures.gff.gz',
#                                names=['chromosome', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'],
#                                 sep='\t')


# ## GWAS table flitering

# In[5]:

def get_dgwas_subset_flt(ddir,fdir):
    dgwas_subset_fltp=f'{ddir}/UKBB/processed/dgwas_subset_flt.pqt'
    if not exists(dgwas_subset_fltp):
        dgwas_subset=pd.read_csv(f'{ddir}/UKBB/raw/I10.gwas.imputed_v3.both_sexes.chr12.tsv',sep='\t',)
        # dgwas=pd.read_csv('/data/UKBB/raw/variants.tsv',sep='\t')

        print(dgwas_subset.shape)
        dgwas_subset_flt=dgwas_subset.loc[~dgwas_subset['low_confidence_variant'],:]
        # dgwas_subset.loc[]
        plt.figure(figsize=[3,3])
        ax=plt.subplot(111)
        ax=dgwas_subset_flt['pval'].apply(np.log10).hist()
        plt.savefig(f'{fdir}/hist_pval.png')
    #     dgwas_subset_flt.to_csv(f'{ddir}/UKBB/processed/dgwas_subset_flt.tsv',sep='\t',)
        dgwas_subset_flt.to_parquet(dgwas_subset_fltp,compression='gzip',
                                   engine='fastparquet')
    else:
        dgwas_subset_flt=pd.read_parquet(dgwas_subset_fltp,engine='fastparquet')
    return dgwas_subset_flt


def get_dgff_regulation_combo(ddir,fdir):
    dgff_regulation_combop=f'{ddir}/ensembl/processed/dgff_regulation_combo.pqt'
    if not exists(dgff_regulation_combop):
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
        plt.figure(figsize=[3,3])
        ax=dgff_regulation_combo['type'].value_counts().plot.barh()
        plt.tight_layout()
    #     plt.savefig('plot/bar_dgff_regulation_combo_type.svg')
        plt.savefig(f'{fdir}/bar_dgff_regulation_combo_type.png')

        dgff_regulation_combo['regulatory_feature_stable_id']=dgff_regulation_combo['attributes'].apply(lambda x : [s.replace('regulatory_feature_stable_id=','') for s in x.split(';') if 'regulatory_feature_stable_id=' in s][0])

        print("number of regulatory elements {len(dgff_regulation_combo['regulatory_feature_stable_id'].unique())}")
        print("number of tissue types {len(dgff_regulation_combo['tissue type'].unique())}")

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
         'regulatory_feature_stable_id']].to_parquet(dgff_regulation_combop,engine='fastparquet',compression='gzip',)
    else:
        dgff_regulation_combo=pd.read_parquet(dgff_regulation_combop,engine='fastparquet')

    return dgff_regulation_combo

def get_dgff_regulation_combo_subset(ddir,dgff_regulation_combo_subset,chromosome='12',tissue_type='Aorta',
                                    fdir):
    dgff_regulation_combo_subsetp=f'{ddir}/ensembl/processed/dgff_regulation_combo.chr{chromosome}.{tissue_type}.pqt'
    if not exists(dgff_regulation_combo_subsetp):
        dgff_regulation_combo_subset=dgff_regulation_combo.loc[((dgff_regulation_combo["tissue type"]==tissue_type) & (dgff_regulation_combo["chromosome"]==chromosome)),:]
        dgff_regulation_combo_subset.to_parquet(dgff_regulation_combo_subsetp,engine='fastparquet',compression='gzip')
    else:
        dgff_regulation_combo_subset=pd.read_parquet(dgff_regulation_combo_subsetp,engine='fastparquet')
    return dgff_regulation_combo_subset
   
def run(ddir):
    dgwas_subset_flt=get_dgwas_subset_flt(ddir)    
    dgff_regulation_combo=get_dgff_regulation_combo(ddir)    
    dgff_regulation_combo_subset=get_dgff_regulation_combo_subset(ddir,dgff_regulation_combo)

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
