#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from glob import glob
from collections import OrderedDict


# In[34]:


###plot the distribution of PPA
def PPAHist(chrs):
    x = fgwas.loc[(fgwas['chr']==chrs), "PPA"]
    print(max(x))
    n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)
    plt.hist(x, bins=bins)
    plt.xlabel('PPA')
    plt.ylabel('count')
    plt.title('Histogram of PPA of fine-mapping region #' + str(chrs))
    plt.grid(True)
    plt.show()


# In[35]:


# PPAHist(12)


# In[81]:


#get the max PPA by each seg
def rankPPA(fgwas, region): 
    print("best fine-mappinig result")
    indices = fgwas.groupby('chunk')['PPA'].idxmax
    print(fgwas.loc[indices])
    print("best GWAS result")
    indices = region.groupby('SEGNUMBER')['pval'].idxmin
    print(region.loc[indices])
    


# In[70]:
# In[76]:
fgwas_output = '/data/analysis/UKBB/result/DeepBind.bfs.gz'

fgwas_nop='/data/analysis/UKBB/processed/test1.bfs.gz'
regionp='/data/analysis/UKBB/processed/I10.gwas.imputed_v3.both_sexes.finemapping.full.tsv.gz'


fgwas=pd.read_csv(fgwas_output,sep=' ')
fgwas_no=pd.read_csv(fgwas_nop,sep=' ')
region = pd.read_csv(regionp,
                    compression='gzip', sep=' ')


#merge the GWAS pvalue with the finemapping 
res = pd.merge(region, fgwas, left_on = 'variant', right_on = 'id')
sub = res.loc[(fgwas['chunk']==0), ]
rankPPA(sub)


# In[71]:


def plotRegion(sub):
    data1 = -np.log10(sub["pval"])
    data2 = sub["PPA"]
    pos = sub["pos_x"]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Position')
    ax1.set_ylabel('-log10(pval)', color=color)
    ax1.scatter(pos, data1, color=color,  label='-log10(pvalue)')
    ax1.tick_params(axis='y', labelcolor=color)
    plt.legend(loc=2)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('PPA', color=color)  # we already handled the x-label with ax1
    ax2.scatter(pos, data2, color=color, label='fine-mapping PPA')
    ax2.tick_params(axis='y', labelcolor=color)
    plt.legend(loc=0)
    ax2.set_ylim(-0.001,0.04)
    ax2.set_xlim(8.24e7,8.27e7)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.show()


# In[72]:


# plotRegion(sub)


# In[75]:


region.loc[(region['pval']==min(region['pval']))]


# In[83]:


rankPPA(fgwas_no, region)

