'''
Purpose: generate the pearson correlation values for all gene pairs in .json format; write to file;

TODO: This script should be wrapped as a POST function to enable generation of correlation values for plot (not yet developed)
'''

import pandas as pd
import numpy as np
from scipy import sparse


def get_correlations(input_df, genes):
    
    data_to_correlate = input_df.loc[genes]   #subset DF to the genes of interest
    correlation_matrix = data_to_correlate.transpose().corr(method='pearson')   #get pearson correlation
    
    output = {'x':[],'y':[],'value':[]}   #create .csv output matrix (input to D3 heatmap)
    for i in correlation_matrix.index:
        for j in correlation_matrix.columns:
            output['x'].append(i)
            output['y'].append(i)
            output['value'].append(correlation_matrix[i][j])

    output_df = pd.DataFrame.from_dict(output)
    output_df.to_csv('test.tsv', index=False)
    return
    
    
df = pd.DataFrame.from_csv('./GeneExpressionAging/data/AM.normcounts.txt',sep='\t', index_col=0)
genes_of_interest = ['ENSMUSG00000000001','ENSMUSG00000000028','ENSMUSG00000000037']

get_correlations(df,genes_of_interest)


