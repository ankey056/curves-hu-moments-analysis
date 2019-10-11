
# curves-hu-moments-analysis

Hu Moments of curves research project

License: MIT

## Usage

`make` command generates data files. After that it is possible to
command `./reform_for_plot.py` for vizualization data creation and
then command `gnuplot ./gnuplot/gui_plot.gp` for vizualization.

### Gnuplot usage

Shortcuts:

+ "Alt-v" - switch vizualization between PCA and ICA
+ "Alt-l" - reload vizualization data
+ "F5" - redraw vizualization
+ "Alt-n" - where n=0..9,  activate n-th contour vizualization
+ "Alt-a" - activate vizualization of all contours together

## Requirements

+ Inkscape is required for bitmap images generating
+ R with fastICA package
+ opencv2
+ python2
+ gnuplot for vizualization
