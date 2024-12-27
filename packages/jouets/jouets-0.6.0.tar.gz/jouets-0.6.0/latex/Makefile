.ONESHELL:

TEX := $(wildcard */*tex)
SVG := $(TEX:.tex=-01.svg)

all: ${SVG} ${PNG}

%-01.svg: %.pdf
	cd $(@D)
	pdf2svg $(*F).pdf $(*F)-%02d.svg all

%.pdf: %.tex
	cd $(@D)
	lualatex $(<F)
