# Treći čas: BPMN, nastavak

Svaka tema ide istim redom: pandan u kodu, mali primjer novog elementa,
zadatak, rješenje i pitanja. Studenti pokušaju zadatak prije rješenja.

## Odgovori na pitanja sa slajdova

### Poruke

- **Koji podatak povezuje odgovor sa narudžbinom?** Broj narudžbine. Svaka
  poruka ga nosi i po njemu stiže baš onoj instanci procesa koja je čeka.
- **Dobavljač odgovori poslije tri dana.** Rok je već prekinuo čekanje i
  nabavka je obavijestila zaposlenog. Poruku više niko ne čeka.

### Čekanje više događaja

- **Gdje dodajete poruku „Odloženo”?** Kao još jednu granu sa porukom iza
  event-based gateway-a.
- **Kada je receive task sa tajmerom dovoljan?** Kada čekamo samo jednu
  vrstu poruke i rok.

### Multi-instance i ponavljanje

- **Možemo li nacrtati AND sa granama za svaku stavku?** Ne. AND traži da
  svaku granu nacrtamo, a broj stavki ne znamo dok proces ne krene.
- **Uslov za izlaz iz petlje** je grana „Potpuna? da”. Bez nje proces
  nikad ne završava.

### Call activity

- **Šta provjera dobija, a šta vraća?** Dobija podatke o dobavljaču, a vraća
  ocjenu: prihvatljiv ili ne. Nabavka po ocjeni bira granu.
- **Gdje stavljate rok?** Boundary tajmer na call activity. Prekida
  provjeru, a nabavka ide granom roka.
- Poziv procesa iz drugog modula ne radimo za kontrolnu tačku. Radimo ga u
  Camundi.

## Kontrolna tačka 1

Dva zadatka na novim primjerima, ne na nabavci. Studenti rade sami.

### Zadatak 1: šta provjeravamo

Jedan model, tekst je na dva slajda. Studenti prvo pročitaju sve, pa crtaju,
jer na papiru ne mogu naknadno dodavati.

- Dva pool-a, Kupac i Servis, povezana porukama: prijava kvara, ponuda,
  odgovor, obavještenje. U servisu lane-ovi Prijem i Tehničar.
- AND za garanciju i dostupnost, a spajanje prije ponude.
- Greška „Serijski broj ne postoji” na granici potprocesa koji obuhvata obje
  provjere.
- Čekanje odgovora na ponudu: event-based gateway sa prihvatanjem,
  odbijanjem i tajmerom od tri dana. Odbijanje i tajmer vode na vraćanje
  laptopa.
- Zamjena i test dijela su multi-instance potproces, jer se dva koraka
  ponavljaju za svaki dio.
- Petlja kontrole kvaliteta: povratak ide u XOR prije popravke, ne direktno
  u task.
- Na potprocesu popravke: tajmer od pet dana koji ne prekida i tajmer od
  deset dana koji prekida. Student treba da objasni šta rok obuhvata.

### Zadatak 2: odgovori

1. Služba prima zahtjev. Ako je prošlo više od 14 dana, šalje odbijanje.
   Inače šalje uputstvo za slanje. Magacin čeka paket, pa pregleda artikal
   po artikal. Za oštećenu robu služba dogovara rješenje sa kupcem. Inače
   se paralelno vraćaju novac i artikli na stanje.
2. 20. dan: grana „ne”, šalje se odbijanje i proces se završava.
3. Tajmer od deset dana prekida čekanje i zahtjev se zatvara.
4. Magacin pregleda tri artikla jedan po jedan. Zatim služba vraća novac,
   a magacin istovremeno vraća artikle na stanje. Proces završava kad su
   oba posla gotova.
