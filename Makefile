# make | make html | make pdf | make YEAR=2025-2026
# Individual lesson: make 2026-2027/vjezbe/class1/class1.pdf
YEAR ?= 2026-2027
COMMON := common
PDF_ENGINE ?= xelatex

# Current lessons have their own directories; older years may use the flat layout.
SRC := $(filter-out %-v1.md %-v2.md %-v3.md %-v4.md,$(wildcard $(YEAR)/vjezbe/class*.md) $(wildcard $(YEAR)/vjezbe/class*/class*.md))
HTML := $(SRC:.md=.html)
PDF := $(SRC:.md=.pdf)
COMMON_CSS = $(shell python3 -c 'import os; print(os.path.relpath("$(COMMON)/slides.css", "$(dir $@)"))')

.PHONY: all html pdf clean
all: html pdf
html: $(HTML)
pdf: $(PDF)

%.html: %.md $(COMMON)/slides.css
	pandoc $< -t revealjs -s -o $@ -V slideNumber=true -V slideLevel=2 \
		-c $(COMMON_CSS) $(EXTRA_CSS)

%.pdf: %.md $(COMMON)/header.tex
	pandoc $< -t beamer -o $@ --pdf-engine=$(PDF_ENGINE) -V theme:metropolis \
		--include-in-header=$(COMMON)/header.tex --resource-path=$(dir $<)

clean:
	rm -f $(HTML) $(PDF)
