#!/opt/R-3.3.1/bin/Rscript

##!/usr/bin/Rscript
##!/opt/R-3.3.1/bin/Rscript
## to run this script
## ./get_d3heatmap_template.R output.html output.json

args <- commandArgs(trailingOnly=TRUE)

# input args for output files and input genes
output_corr_d3heatmap_html <- args[1]
output_corr_d3heatmap_json <- args[2]

#the following is for future development
#selected_features_infile   <- args[3]
#selected_samples_infile    <- args[4]

# to generate d3heatmap template for correlation heatmaps
# libs
library(data.table)
library(dplyr)
library(plotly)
library(d3heatmap)
library(htmlwidgets)
options(tibble.width = Inf)

# reference
# https://raw.githubusercontent.com/rstudio/d3heatmap/master/tests/smoketest.R
serialize <- function(widget) {
      htmlwidgets:::toJSON2(widget, pretty=TRUE, digits = 12)
}

`%+%` <- function(x, y) paste0(x, y)

get_d3heatmap_template_and_json <- function(data, 
                                            selected_features=NULL, 
                                            selected_samples=NULL, 
                                            k_row=3,
                                            k_col=3, ...){

    if (is.null(selected_samples)) {
        selected_samples <- setdiff(colnames(data), 'gene_ensembl')
    }

    if (is.null(selected_features)) {
        selected_features <- data$gene_ensembl
    }

    cor.data <- as.data.frame(data) %>%
    dplyr::filter(gene_ensembl %in% selected_features) %>%
    dplyr::select(one_of(selected_samples)) %>%
    as.matrix

    # for template usage, just randomly select 50 features
    cor <- cor.data %>%
    t %>%
    cor(method='pearson', use='complete.obs')

    colnames(cor) <- selected_features
    rownames(cor) <- selected_features

    # set 3 cluster both row-wise and col-wise for now
    d <- d3heatmap::d3heatmap(cor, k_row=k_row, k_col=k_col)
    json <- serialize(d)

    return(list(d3heatmap.obj=d, json=json))
}


# example on using the function
if (TRUE)  {     # load data for template
    data <- fread(file.path('../data/norm_data/norm_all.csv'), header=TRUE, stringsAsFactors=FALSE)
    meta <- fread(file.path('../data/norm_data/norm_metadata.csv'), header=TRUE, stringsAsFactors=FALSE)

    dim(data)

    selected_features <- data$gene_ensembl[1:40] # temp choice to randomly select 40 genes
    selected_samples  <- setdiff(colnames(data), 'gene_ensembl')

    #selected_features <- scan(file=file.path(selected_features_infile), what=character())
    #selected_samples  <- scan(file=file.path(selected_samples_infile), what=character())

}    # End load data


ret <- get_d3heatmap_template_and_json(data, selected_features, selected_samples)
names(ret)
print( "correlation d3 heatmap html has been outputted to " %+% output_corr_d3heatmap_html ) 
print( "correlation d3 heatmap json has been outputted to " %+% output_corr_d3heatmap_json ) 

write(ret$json, file=file.path(output_corr_d3heatmap_json))
htmlwidgets::saveWidget(as_widget(ret$d3heatmap.obj), file.path(output_corr_d3heatmap_html), selfcontained=FALSE)

