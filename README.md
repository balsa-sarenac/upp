# Upravljanje poslovnim procesima

- [Vježbe 2026–2027](2026-2027/README.md)
- [Vježbe 2025–2026](2025-2026/README.md)

## Prezentacije

Prezentacije se pišu u Markdown-u (`<godina>/vjezbe/classN.md`) i
kompajliraju u HTML (reveal.js) i PDF (beamer). Iz korijena repozitorijuma:

```
make                         # sve prezentacije za tekuću godinu
make html                    # samo HTML
make pdf                     # samo PDF
make YEAR=2025-2026          # druga školska godina
make 2026-2027/vjezbe/class1.pdf
```

Zajednički stil i LaTeX zaglavlje su u direktorijumu `common/`.

Potrebni su `pandoc`, `make` i, za PDF, LaTeX sa temom metropolis:

```
tlmgr install beamertheme-metropolis
```

Umjesto `xelatex` može i `lualatex`: `make pdf PDF_ENGINE=lualatex`.

## Troubleshooting

Za PDF verziju potreban je font koji podržava ćirilicu.
Trenutno se koristi font [DejaVu Sans](https://dejavu-fonts.github.io/).
