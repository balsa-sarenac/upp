# Upravljanje poslovnim procesima

## Vježbe 2027-2028

Potreban softver: [Camunda 8](https://docs.camunda.io/)

Materijali su kopija generacije 2026-2027. Prva tri časa ćemo
preraspodijeliti tako da treći čas ostane rasterećen za kontrolnu tačku.
Pravila za izradu materijala su u [pravila.md](pravila.md).

## Nova raspodjela prva tri časa

| Čas | Teme | Šta se seli |
| --- | --- | --- |
| 1 | Uvod: kod ili model, osnovni elementi, pool, lane i poruke. XOR i AND. | XOR i AND dolaze iz 2. časa. |
| 2 | Vrste zadataka i događaja, tajmeri, potproces i greška. Petlja preko XOR-a i call activity unutar modula. | Petlja i call activity dolaze iz 3. časa. Dodatak sa odgovorom dobavljača je izbačen. |
| 3 | Poruke između dva učesnika, event-based gateway i multi-instance. Kontrolna tačka 1. | Ostaje samo ono što traži poruke i liste, pa više vremena ide na kontrolnu tačku. |

Zašto ovako:

- XOR i AND su osnova svakog modela, pa ih studenti vježbaju od prvog
  časa.
- Petlja je samo XOR koji vraća proces nazad, a call activity je blizak
  potprocesu. Oba se prirodno nastavljaju na 2. čas.
- Poruke, event-based gateway i multi-instance traže dva učesnika ili
  listu. Zajedno čine jednu cjelinu na 3. času.

## Šta je urađeno

- 1. čas: dodati su početak i kraj, gateway-i, XOR, AND, zadatak A sa
  rješenjem i dvije česte greške sa XOR i AND. Prijava ispita je domaći.
- 2. čas: počinje rješenjem A. Dodati su petlja i call activity sa 3. časa.
  Dodatak sa odgovorom dobavljača je izbačen, i iz kataloga dijagrama.
- 3. čas: bez petlje i call activity-ja. Kontrolna tačka 1 se radi na času.
- Napomene: 3. čas ima ishode, plan i samoprovjeru; 2. čas ima odgovore za
  petlju i call activity.

## Šta treba uraditi

- Napomene za 1. i 2. čas: ishodi, plan i samoprovjera.
- Generatori dijagrama u `tools/bpmn/` pišu u 2026-2027. Za novu
  generaciju treba im zadati folder.
- Dijagrami petlje i call activity-ja su u `class3/bpmn-class3/`, a koristi
  ih 2. čas.

## Prvi čas

- [Prezentacija (HTML)](vjezbe/class1/class1.html) · [PDF](vjezbe/class1/class1.pdf)

## Drugi čas

- [Prezentacija (HTML)](vjezbe/class2/class2.html) · [PDF](vjezbe/class2/class2.pdf)
- [BPMN dijagrami](vjezbe/class2/bpmn-class2/README.md)

## Treći čas

- [Prezentacija (HTML)](vjezbe/class3/class3.html) · [PDF](vjezbe/class3/class3.pdf)
- [BPMN dijagrami](vjezbe/class3/bpmn-class3/README.md)
- [Napomene za nastavnika](vjezbe/class3/napomene-class3.md)

Izgradnja: `make YEAR=2027-2028`.
