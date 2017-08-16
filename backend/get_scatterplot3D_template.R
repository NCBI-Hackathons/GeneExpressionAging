#!/usr/local/bin/Rscript

#to generate the plotly output for the PCA plot

#libraries
library(plotly)
library(rjson)
library(RColorBrewer)

#function
render_pca_plot_json <- function(data, metadata, variable_of_interest, genes_of_interest){
  
  color_list = c('#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd') #http://colorbrewer2.org/?type=qualitative&scheme=Set3&n=10
  
  #re-order the data to match colnames and rownames
  data <- data[,colnames(data) %in% rownames(metadata)]
  metadata <- metadata[rownames(metadata) %in% colnames(data),]
  ord <- match(colnames(data), rownames(metadata))
  metadata <- metadata[ord, ]
  
  data <- data[complete.cases(data),]
  
  sub_data <- NULL
  if(length(genes_of_interest) > 1){
    sub_data <- data[rownames(data) %in% genes_of_interest,]   #subset into only the genes of interest
  }else{
    sub_data <- data                                         #don't subset, use all genes in the correlation
  }
  X <- prcomp(scale(t(sub_data),center=TRUE,scale=TRUE))   #run PCA on scaled data
  pca_result <- as.data.frame(X$x[,1:3])
  pca_result$color <- color_list[as.factor(metadata[,variable_of_interest])]
  color <- as.factor(metadata[,variable_of_interest])   #append the color-value based on the variable of interest
  pca_result$id <- rownames(metadata)                  #create ID variable to be shown in the hover object
  pca_result$color <- color_list[as.factor(metadata[,variable_of_interest])]

  #write to .csv to load in pure plotly.js 
  write.csv(pca_result,"PCAscatterplot.csv", quote=FALSE)    #TODO: this can be removed once it's hooked up to directly feed .json to the front end
}

args = commandArgs(trailingOnly=TRUE)   #user supplies arguments

main <- function(A, B){
  
  #inputs from the user
  data <- read.csv(A, row.names=1)   
  metadata <- read.csv(B, row.names=1) 
  variable_of_interest <- 'flu'
  genes_of_interest <- rownames(data)[1:1000]
  
  #run the plot
  render_pca_plot_json(data, metadata, variable_of_interest, genes_of_interest)
}

#for testing purposes...
#A <- "/Users/kkalantar/Documents/GradSchool/NCBIhackathon/GeneExpressionAging/data/am.shuff.log.counts.csv"
#B <-"/Users/kkalantar/Documents/GradSchool/NCBIhackathon/GeneExpressionAging/data/norm_data/norm_metadata.csv"
#main(A,B)

#to run from Rscript 
main(args[1],args[2])

