# Upravljanje poslovnim procesima

## Vježbe 2026–2027

Vježbe obuhvataju oko deset termina od po 90 minuta. Koristimo Camunda
platformu i zajednički primjer zahtjeva za nadoknadu troškova sa priloženim
računom. Manje vježbe i implementacije radimo i ocjenjujemo na času,
umjesto velikog projekta za rad kod kuće.

| Sedmica | Tema i rad na času | Provjera |
| --- | --- | --- |
| 1 | BPMN: učesnici, saradnja i tokovi poruka | |
| 2 | Grananja, paralelizam i događaji | |
| 3 | Potprocesi i izuzeci | Individualno BPMN modelovanje |
| 4 | Camunda: forme, promjenljive i ljudski zadaci | |
| 5 | Servisna integracija i izvršavanje malog procesa | Individualna provjera implementacije |
| 6 | AI pomoć u razvoju: generisanje i pregled modela, nedostajući zahtjevi i greške | |
| 7 | AI integracija: izdvajanje podataka iz dokumenta ili klasifikacija | |
| 8 | Validacija izlaza, ljudski pregled i obrada neuspjeha | |
| 9 | Zaokruživanje AI integracije | Individualna praktična provjera |
| 10 | Povratne informacije i preostale provjere | Ponovna provjera znanja |

Tri kontrolne tačke provjeravaju modelovanje, izvršavanje i AI integraciju.
Svaki student kratko demonstrira i objašnjava svoje rješenje na času,
uz individualnu varijaciju zajedničkog primjera. Raspodjela poena biće
objavljena uz kriterijume provjera.

[Uvodna prezentacija i prva vježba](vjezbe/class1.md) predstavljaju plan rada.
Izbor verzije i nastavnog okruženja za Camunda platformu, kao i uputstvo
za pristup, biće objavljeni prije dijela o izvršavanju procesa.

## Prezentacije
Komande se pokreću iz direktorijuma `vjezbe`. Prezentacije se kompajliraju sa:

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

## Troubleshooting

Za pdf verzija potreban je font koji podržava ćirilicu.
Trenutno se koristi font [DejaVu Sans](https://dejavu-fonts.github.io/).
