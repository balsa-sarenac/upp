# make | make html | make pdf | make YEAR=2025-2026
# Individual lesson: make 2026-2027/vjezbe/class2/class2.pdf
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
	pandoc $< -t revealjs -s -o $@ -V slideNumber=true --slide-level=2 \
		-c $(COMMON_CSS) $(EXTRA_CSS)

%.pdf: %.md $(COMMON)/header.tex
	pandoc $< -t beamer -o $@ --pdf-engine=$(PDF_ENGINE) -V theme:metropolis \
		--include-in-header=$(COMMON)/header.tex --resource-path=$(dir $<)

clean:
	rm -f $(HTML) $(PDF)

CLASS2 := $(YEAR)/vjezbe/class2
$(CLASS2)/class2.html $(CLASS2)/class2.pdf: $(wildcard $(CLASS2)/bpmn-class2/*.svg)
$(CLASS2)/class2.html: EXTRA_CSS = -c class2.css
$(CLASS2)/class2.html: $(CLASS2)/class2.css

CLASS3 := $(YEAR)/vjezbe/class3
$(CLASS3)/class3.html: EXTRA_CSS = -c class3.css
$(CLASS3)/class3.html: $(CLASS3)/class3.css
$(CLASS3)/class3.html $(CLASS3)/class3.pdf: $(wildcard $(CLASS3)/bpmn-class3/*.svg)

# From 2027-2028 class 1 reuses class 2 diagrams, so it needs the same image styling.
2027-2028/vjezbe/class1/class1.html: EXTRA_CSS = -c ../class2/class2.css
2027-2028/vjezbe/class1/class1.html: 2027-2028/vjezbe/class2/class2.css

# Archived drafts are built only when explicitly requested.
ARCHIVE := $(CLASS2)/archive
$(ARCHIVE)/class2-v1.html $(ARCHIVE)/class2-v2.html: EXTRA_CSS = -c class2.css
$(ARCHIVE)/class2-v1.html $(ARCHIVE)/class2-v2.html: $(ARCHIVE)/class2.css
$(ARCHIVE)/class2-v3.html: EXTRA_CSS = -c class2-v3.css
$(ARCHIVE)/class2-v3.html: $(ARCHIVE)/class2-v3.css
$(ARCHIVE)/class2-v4.html: EXTRA_CSS = -c class2-v4.css
$(ARCHIVE)/class2-v4.html: $(ARCHIVE)/class2-v4.css

.PHONY: preview
preview:
	python3 tools/preview.py --class $(or $(CLASS),class2)
