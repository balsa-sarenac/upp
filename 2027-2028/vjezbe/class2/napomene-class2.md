# Drugi čas: događaji, potproces, petlja i call activity

Čas počinje rješenjem zadatka A sa prvog časa. Zadatak B ga proširuje
greškom i rokovima. Na kraju dolaze petlja i call activity, koji su ranije
bili na 3. času.

## Odgovori na pitanja sa slajdova

### Petlja

- **Uslov za izlaz iz petlje** je grana „Potpuna? da”. Bez nje proces
  nikad ne završava.
- Povratak ide u XOR prije taska, ne direktno u task.

### Call activity

- **Šta provjera dobija, a šta vraća?** Dobija podatke o dobavljaču, a vraća
  ocjenu: prihvatljiv ili ne. Nabavka po ocjeni bira granu.
- **Gdje stavljate rok?** Boundary tajmer na call activity. Prekida
  provjeru, a nabavka ide granom roka.
- Poziv procesa iz drugog modula ne radimo za kontrolnu tačku. Radimo ga u
  Camundi.

## Šta još nedostaje

Ishodi učenja, plan časa i samoprovjera. Stare napomene drugog časa
(2026-2027, arhiva, van git-a) imaju dobar plan za zadatke A i B.
