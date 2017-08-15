
# to generate d3heatmap template for correlation heatmaps


## libs
library(data.table)
library(plyr)
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



get_d3heatmap_template_and_json <- function(data, 
                                            selected_features=NULL, 
                                            selected_samples=NULL, 
                                            k_row=3,
                                            k_col=3, ...){

    if (is.null(selected_samples)) {
        selected_samples <- setdiff(colnames(data), 'ensembl')
    }

    if (is.null(selected_features)) {
        selected_features <- data$ensembl
    }

    cor.data <- as.data.frame(data) %>%
    dplyr::filter(ensembl %in% selected_features) %>%
    dplyr::select(one_of(selected_samples)) %>%
    as.matrix

    #rownames(cor.data) <- selected_features
    #colnames(cor.data) <- selected_samples

    # for template usage, just randomly select 50 features
    cor <- cor.data %>%
    t %>%
    cor(method='pearson')

    colnames(cor) <- selected_features
    rownames(cor) <- selected_features

    # set 3 cluster both row-wise and col-wise for now
    d <- d3heatmap::d3heatmap(cor, k_row=k_row, k_col=k_col)
    json <- serialize(d)

    return(list(d3heatmap.obj=d, json=json))
}



# example on using the function
if (TRUE)  {     # load data for template
    dat  <- fread(file.path('../data/lung.shuff.log.counts.csv'), header=TRUE, stringsAsFactors=FALSE)
    meta <- fread(file.path('../data/column_components.csv'), header=TRUE, stringsAsFactors=FALSE)
    selected_features <- dat$ensembl[1:20]
    selected_samples <- setdiff(colnames(data), 'ensembl')
}    # End load data

ret <- get_d3heatmap_template_and_json(dat, selected_features, selected_samples)

names(ret)

write(ret$json, file=file.path('../webcomponents/src/corr-d3heatmap/template_corr_d3heatmap.json'))

htmlwidgets::saveWidget(as_widget(ret$d3heatmap.obj), 
                        file.path("/home/freeman/github/GeneExpressionAging/webcomponents/src/corr-d3heatmap/template_corr_d3heatmap.html"), 
                        selfcontained=FALSE)
                        #file.path('../webcomponents/src/corr-d3heatmap/template_corr_d3heatmap.html'), 
                        #file.path("/home/freeman/github/GeneExpressionAging/webcomponents/src/corr-d3heatmap/template_corr_d3heatmap.html"), 


#----------------------------------------------------------------------------
output_name <- 'test'
`%+%` <- function(x, y) paste0(x, y)

if (FALSE) {    # debug
    data              <- dat
    selected_features <- dat$ensembl[1:20]
    selected_samples  <- setdiff(colnames(data), 'ensembl')
    k_row             <- 3
    k_col             <- 3
}    # End 

