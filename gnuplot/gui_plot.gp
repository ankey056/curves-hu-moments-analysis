
set terminal wxt persist enhanced size 600, 480

datDirBase = "./output/trajectories/group"

allModeTitleCode = "if (allmode == 0) \
{ group_title = sprintf(\"%d. %s\", group_number, group_name); } \
else { group_title = 'All data'; };"

loadDataGroup(n) = sprintf("group_index = %d; \
                            load sprintf(\"%s-%%.3d/init.gp\", \
                                         group_index) ; \
                            %s \
                            eval plotcmd(0) ;", n, datDirBase, allModeTitleCode);

datTemplate(s) = sprintf("%s-%%.3d/%s_trajectory_%%.3d.dat", \
                         datDirBase, s)

pcadatfile(gi, i) = sprintf(datTemplate("PCA"), \
                            gi, i)

icadatfile(gi, i) = sprintf(datTemplate("ICA"), \
                            gi, i)

vizmode = 0

unset multiplot

vizcmd1 (titlep, datfun) = sprintf("set title '%s' ; \
\
    plot for [i=1:tcount] %s(group_index, i) using 1:2:3:4 with vectors \
         title columnhead ; ", \
  titlep, datfun)

vizall(titlep, datfun) =  sprintf("set title '%s'; \
datfile(gi, i) = %s(gi, i); \
load './output/trajectories/plot_all.gp';", titlep, datfun);

vizcmd(titlep, datfun) = sprintf("if (allmode == 0) \
{ eval vizcmd1('%s', '%s'); } \
else { eval vizall('%s', '%s'); } ;", \
                                   titlep, datfun, titlep, datfun)


plotcmd(x) = sprintf("load \"./gnuplot/plotcmd_%d.lib.gp\"", vizmode)


## vizualization mode switching
## vizmode = 0 - PCA and ICA plot
## vizmode = 1 - PCA plot
## vizmode = 2 - ICA plot
bind "alt-v" "eval \"if (vizmode == 0) { \
   vizmode = 1; \
   } else { \
     if (vizmode == 1) { \
        vizmode = 2; \
        } else { vizmode = 0; } } ; \
   eval plotcmd(0) ; \" ;"

allmode = 0
bind "alt-a" "eval sprintf(\"if (allmode == 0) { \
   allmode = 1; } else { allmode = 0 } ; \
   %s \
   eval plotcmd(0) ; \", allModeTitleCode) ;"


bind "F5" "eval plotcmd(0);"
bind "alt-l" 'load "./output/trajectories/init.gp" ;'

load "./output/trajectories/init.gp"
