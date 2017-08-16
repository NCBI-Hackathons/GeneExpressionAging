#!/opt/R-3.3.1/bin/Rscript

# build a template for gene mapping table via DT(datatable) package

library(DT)
library(data.table)
library(dplyr)
options(tibble.width = Inf)

if (TRUE)  {    # load data
    genemap <- fread(file.path('../data/mouse_geneid_map_GRCm38_081517.csv'), header=TRUE, stringsAsFactors=FALSE)
}


## data manipulation
dat.dt <- genemap %>%
dplyr::arrange(chromosome_name, start_position) %>%
dplyr::mutate(entrezgene = ifelse(is.na(entrezgene), '', entrezgene)) %>%
dplyr::mutate(url_entrezgene=paste0('<a href="https://www.ncbi.nlm.nih.gov/gene/', entrezgene, '" target="_blank">', entrezgene, '</a>')) %>% 
dplyr::mutate(url_ensembl=paste0('<a href="http://www.ensembl.org/Mus_musculus/Gene/Summary?g=', ensembl_gene_id, '" target="_blank">', ensembl_gene_id, '</a>')) %>%
dplyr::select(gene_symbol=external_gene_name, 
              ensembl_gene_id=url_ensembl, 
              entrez_gene_id=url_entrezgene, 
              chromosome=chromosome_name, 
              start_position, end_position) %>%
unique %>%
head(1000)  # table first 1000 data as an lit example


## output datatable htmlfile
dt <- datatable(dat.dt, options=list(pageLength = 20, AutoWidth=TRUE), caption = ' ',  escape = FALSE)
DT::saveWidget(dt, 
               '/home/freeman/github/GeneExpressionAging/webcomponents/src/genemap-datatable/mouse_geneid_map_GRCm38_081517_lit.html',
               selfcontained=FALSE)

## output json file
serialize <- function(widget) {
      htmlwidgets:::toJSON2(widget, pretty=TRUE, digits = 12)
}

json <- serialize(dt)
write(json, '/home/freeman/github/GeneExpressionAging/webcomponents/src/genemap-datatable/mouse_geneid_map_GRCm38_081517_lit.json') 


