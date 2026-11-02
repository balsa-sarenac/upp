# Upravljanje poslovnim procesima

- [Vježbe 2026–2027](2026-2027/README.md)
- [Vježbe 2025–2026](2025-2026/README.md)

## Prezentacije

Prezentacije se pišu u Markdown-u (`<godina>/vjezbe/classN/classN.md`) i
kompajliraju u HTML (reveal.js) i PDF (beamer). Iz korijena repozitorijuma:

```
make                         # sve prezentacije za tekuću godinu
make html                    # samo HTML
make pdf                     # samo PDF
make YEAR=2025-2026          # druga školska godina
make 2026-2027/vjezbe/class1/class1.pdf
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

Za SVG dijagrame u prezentaciji drugog časa potreban je i `rsvg-convert`
(iz paketa librsvg) pri izgradnji PDF-a. HTML koristi izvorne SVG slike.

## Uređivanje uz automatski pregled

Pokrenite `make preview`. Pregled se otvara u pregledaču. Uređujte
`2026-2027/vjezbe/class2/class2.md` u svom editoru i sačuvajte promjenu.
HTML se obnavlja automatski, a pregled ostaje na istom slajdu.
Za prvi čas koristite `make preview CLASS=class1`. Zaustavljanje: Ctrl+C.

PDF izvezite kada završite: `make pdf`. Zadaci u `zadatak-class2.md`
uređuju se zasebno. `tools/bpmn/slides.py` čuva prvobitni generator i
ne prepisuje ručne izmjene bez izričite opcije `--overwrite`.
