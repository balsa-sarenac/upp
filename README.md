# Upravljanje poslovnim procesima

## Prezentacije
Prezentacije se kompajliraju sa:

```
pandoc class1.md -t revealjs -s -o class1.html -V slideNumber=true -V slideLevel=2 -c slides.css
```

Za pdf verziju je potrebno da se instalira tema:
```
tlmgr install beamertheme-metropolis
```

```
pandoc class1.md -t beamer -o class1.pdf --pdf-engine=xelatex -V theme:metropolis --include-in-header=header.tex
```

(umjesto `xelatex` moze i `lualatex`)

## Projeka

Projekat se kompajlira sa:

```
pandoc projekat.md -o projekat.pdf --pdf-engine=xelatex --include-in-header=header.tex
```

## Troubleshooting

Za pdf verzija potreban je font koji podržava ćirilicu.
Trenutno se koristi font [DejaVu Sans](https://dejavu-fonts.github.io/).
