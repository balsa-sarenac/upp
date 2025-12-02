# Upravljanje poslovnim procesima

## Prezentacije
Prezentacije se kompajliraju sa:

```
pandoc class1.md -t revealjs -s -o class1.html -V slideNumber=true -V slideLevel=2 -c slides.css
```

ili za pdf verziju:

```
pandoc class1.md -t beamer -o class1.pdf --pdf-engine=lualatex
```

(umjesto `lualatex` moze i `xelatex`)

## Projekat

Projekat se kompajlira sa:

```
pandoc projekat.md -o projekat.pdf --pdf-engine=lualatex
```

## Troubleshooting

Za pdf verzija potreban je font koji podržava ćirilicu.
Trenutno se koristi font [DejaVu Sans](https://dejavu-fonts.github.io/).
