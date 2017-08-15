
# to generate d3heatmap template for correlation heatmaps


## libs
library(plyr)
library(dplyr)
library(d3heatmap)
options(tibble.width = Inf)

# reference
# https://raw.githubusercontent.com/rstudio/d3heatmap/master/tests/smoketest.R
serialize <- function(widget) {
      htmlwidgets:::toJSON2(widget, pretty=TRUE, digits = 12)
}

mock_d3heatmap_record <- function(...) {
    cat(format(sys.call(0)), "\n")
    d <- d3heatmap::d3heatmap(...)
    json <- serialize(d$x)
    cat(json, "\n")
}


if (TRUE)  {     # load data for template
    dat  <- fread(file.path('../data/lung.cleaned.log.counts.csv'), header=TRUE, stringsAsFactors=FALSE)
    meta <- fread(file.path('../data/column_components.csv'), header=TRUE, stringsAsFactors=FALSE)
}    # End load data


# for template usage, just randomly select 50 features
cor <- dat[, 1:51] %>% 
dplyr::select(-ensembl) %>% 
as.data.frame %>%
cor(method='pearson')

# set 3 cluster both row-wise and col-wise for now
d <- d3heatmap::d3heatmap(cor, k_row=3, k_col=3)
json <- serialize(d$x)
json

write(json, file=file.path('./webcomponents/src/corr-d3heatmap/template_corr_d3heatmap.json'))

htmlwidgets::saveWidget(as_widget(d), 
                        file.path("./webcomponents/src/corr-d3heatmap/template_corr_d3heatmap.html"), 
                        selfcontained=FALSE)


