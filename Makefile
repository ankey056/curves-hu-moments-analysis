
all: output/pca-ica-analysis.dat

output/painted-contours-hu.dat: input/input.svg generate_bitmaps.py compute_hu_moments.py
	mkdir -p ./tmp/marked/ ./output/
	./generate_bitmaps.py $< ./tmp/ && ./compute_hu_moments.py > $@

output/pca-ica-analysis.dat: pca_ica_analysis.R output/painted-contours-hu.dat
	Rscript $<

.PHONY: clean
clean:
	rm -rf ./tmp/ ./output/

