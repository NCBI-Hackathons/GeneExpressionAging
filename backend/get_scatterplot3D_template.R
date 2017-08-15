
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

  if(length(genes_of_interest) > 1){
    sub_data <- data[rownames(data) %in% genes_of_interest,]   #subset into only the genes of interest
  }else{
    sub_data <- data   #don't subset
  }
  X <- prcomp(scale(t(sub_data),center=TRUE,scale=TRUE))   #run PCA on scaled data
  pca_result <- as.data.frame(X$x[,1:3])
  pca_result$color <- as.factor(metadata[,variable_of_interest])   #append the color-value based on the variable of interest

  pca_result$id <- rownames(metadata)
  #render plotly
  p <- plot_ly(pca_result, x = ~PC1, y = ~PC2, z = ~PC3, color = ~color, colors = color_list[seq(1:length(levels(factor(metadata[,variable_of_interest]))))], text= ~id) %>%
    add_markers() %>%
    layout(scene = list(xaxis = list(title = 'PC1'),
                        yaxis = list(title = 'PC2'),
                        zaxis = list(title = 'PC3')))
  
  #convert plotly object to .json to be loaded into viewer
  write(plotly_json(p)[1]$x$data,"json_output.json")    #TODO: this can be removed once it's hooked up to directly feed .json to the front end
  return(plotly_json(p)[1]$x$data)   #return .json object
}


#inputs from the user
data <- read.csv("/Users/kkalantar/Documents/GradSchool/NCBIhackathon/GeneExpressionAging/data/am.cleaned.log.counts.csv")
metadata <- read.csv("/Users/kkalantar/Documents/GradSchool/NCBIhackathon/GeneExpressionAging/data/column_components.csv",row.names=1)
variable_of_interest <- 'replica'
genes_of_interest <- rownames(data)[1:100]

render_pca_plot_json(data, metadata, variable_of_interest, genes_of_interest)

