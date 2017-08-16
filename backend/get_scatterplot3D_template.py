
'''
Purpose: This script generates the PCAscatterplot.csv file that is currently being loaded in the PCA tab of the viewer.

Run as follows:
python get_scatterplot3D_template.py [counts table filepath] [metadata filepath] 

Note: No genes are used for subsetting and the variable of interest is set to 'flu'.

TODO:
This script should be wrapped into a POST call that takes the user input gene list and user input variable of interest for coloring to enable interactive re-generation of the PCA plot. Currently the PCA plot is static.

'''


import sys
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

def run_pca(data_file, metadata_file, variable_of_interest, genes_of_interest = None):

    #default colors
    color_list = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd'] #http://colorbrewer2.org/?type=qualitative&scheme=Set3&n=10

    df = pd.read_csv(data_file, index_col=0)   #read data into dataframe
    
    if(genes_of_interest):
        df = df.loc[genes_of_interest]   #subset dataframe given list of input genes

    metadata = pd.read_csv(metadata_file, index_col=0)  #read in metadata
    m = metadata.loc[df.columns]    #select only the metadata rows for which we have data in dataframe

    #catch error if the rownames don't match the data columns...
    #TODO: deal with this by sorting dataframes instead of throwing error - then procceed. 
    #Didn't address this yet due to time limitations.
    if(sum(m.index != df.columns) > 0):
        print("ERROR: rows of metadata are not in the same order as columns from counts matrix")
        return
    
    #create categorical variable for color scheme
    s = list(set(m[variable_of_interest]))
    color_map = dict(zip( s, color_list[0:len(s)] )) 

    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(df.transpose())

    #create output for .csv
    pca_df = pd.DataFrame(pca_result)
    pca_df.columns = ['PC1','PC2','PC3']
    pca_df['id'] = [i for i in df.columns]
    pca_df['colors'] = [color_map[i] for i in m[variable_of_interest]]
    
    pca_df.to_csv('PCAscatterplot.csv',index=False)

data_file = sys.argv[1]
metadata_file = sys.argv[2]
variable_of_interest = 'flu'  #eventually make this input from user

run_pca(data_file, metadata_file, variable_of_interest)
 
