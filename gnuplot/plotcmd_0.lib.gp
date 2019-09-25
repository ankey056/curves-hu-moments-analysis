
set multiplot layout 1,2 title group_title

eval vizcmd('PCA', 'pcadatfile') ;

eval vizcmd('ICA', 'icadatfile') ;

unset multiplot

# refresh ;