#!/opt/R-3.3.1/bin/Rscript

if (FALSE) {    # install pkgs
    source("http://bioconductor.org/biocLite.R")
    biocLite("biomaRt")

    install.packages('data.table')
    install.packages('tidyverse')
}    


## libs
library(biomaRt)
library(data.table)
library(tidyverse)
options(tibble.width = Inf)

## biomaRt
ensembl <- useEnsembl(biomart="ensembl", dataset="mmusculus_gene_ensembl")
(attr.tmp <- listAttributes(ensembl))

all_chr_genes <- getBM(attributes=c('ensembl_gene_id', 'ensembl_transcript_id', 
                                    'hgnc_symbol', 'hgnc_id', 
                                    'external_gene_name',
                                    'entrezgene',
                                    'chromosome_name', 'start_position', 'end_position'), 
                       mart = ensembl)

ret <- all_chr_genes %>%
dplyr::mutate(url_entrezgene=paste0('<a href="https://www.ncbi.nlm.nih.gov/gene/', entrezgene, '" target="_blank">', entrezgene, '</a>')) %>% 
dplyr::mutate(url_ensembl=paste0('<a href="http://grch37.ensembl.org/Mouse/Gene/Summary?g=', ensembl_gene_id, '" target="_blank">', ensembl_gene_id, '</a>'))

ret %>% dplyr::filter(!is.na(entrezgene)) %>% head

write.csv(ret, file=file.path('../data/mouse_geneid_map_grch37_081417.csv'), row.names=FALSE)


