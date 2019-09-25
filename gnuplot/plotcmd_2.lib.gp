

unset multiplot

# eval vizcmd('PCA', 'pcadatfile')
eval vizcmd(sprintf("%s. ICA", group_title), \
            'icadatfile')