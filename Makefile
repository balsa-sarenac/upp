# Prezentacije za vježbe: vjezbe/classN.md -> classN.html i classN.pdf
#
#   make                      sve prezentacije za tekuću godinu
#   make html | make pdf      samo jedan format
#   make YEAR=2025-2026       druga školska godina
#   make 2026-2027/vjezbe/class1.pdf

YEAR ?= 2026-2027
COMMON := common
PDF_ENGINE ?= xelatex

SRC  := $(wildcard $(YEAR)/vjezbe/class*.md)
HTML := $(SRC:.md=.html)
PDF  := $(SRC:.md=.pdf)

.PHONY: all html pdf clean
all: html pdf
html: $(HTML)
pdf: $(PDF)

# HTML upućuje na CSS relativno, jer su sve prezentacije u <godina>/vjezbe/
%.html: %.md $(COMMON)/slides.css
	pandoc $< -t revealjs -s -o $@ -V slideNumber=true -V slideLevel=2 \
		-c ../../$(COMMON)/slides.css

%.pdf: %.md $(COMMON)/header.tex
	pandoc $< -t beamer -o $@ --pdf-engine=$(PDF_ENGINE) -V theme:metropolis \
		--include-in-header=$(COMMON)/header.tex --resource-path=$(dir $<)

clean:
	rm -f $(HTML) $(PDF)
