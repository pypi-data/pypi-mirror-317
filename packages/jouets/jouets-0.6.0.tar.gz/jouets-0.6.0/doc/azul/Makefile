GIF := maximal.gif T.gif ligne.gif

all: ${GIF}

%.pdf: %.tex
	lualatex $<

%.gif: %.pdf
	convert -verbose -delay 50 -loop 0 -density 300 -resize 200 $< $@
