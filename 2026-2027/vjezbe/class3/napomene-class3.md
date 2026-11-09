# Treći čas: BPMN, nastavak

Svaka tema ide istim redom: pandan u kodu, mali primjer novog elementa,
zadatak, rješenje i pitanja. Ove godine zadatke sa slajdova studenti rade
kao domaći i tako vježbaju za kontrolnu tačku. Na času pokazujemo primjer,
kratko razgovaramo o zadatku i prolazimo rješenje.

## Ishodi učenja

Poslije časa student može da:

1. Nacrta dva učesnika koji razmjenjuju poruke: send task, receive task,
   message start event i message flow između pool-ova.
2. Objasni kako poruka stiže baš onoj instanci procesa koja je čeka: po
   broju (ID) koji poruka nosi.
3. Izabere event-based gateway kada proces čeka jedan od više događaja, i
   receive task sa tajmerom kada čeka samo jednu poruku i rok.
4. Upotrijebi multi-instance kada broj ponavljanja zavisi od liste, i
   izabere paralelno ili sekvencijalno izvršavanje.
5. Nacrta petlju preko XOR-a, tako da povratak ne ulazi direktno u task.
6. Razlikuje potproces od call activity-ja i kaže šta pozvani proces dobija,
   a šta vraća.

## Plan časa

| Okvirno | Dio časa | Šta rade studenti |
| --- | --- | --- |
| 10 min | Prethodni čas: rješenje B | Prate jedan scenario na rješenju B |
| 20 min | Poruke | Čitaju primjer upita za cijenu, zatim prolazimo zadatak i rješenje |
| 15 min | Event-based gateway | Porede receive task sa tajmerom i event-based gateway |
| 20 min | Multi-instance i petlja | Kažu zašto AND ne radi za listu; nalaze uslov za izlaz iz petlje |
| 10 min | Call activity | Kažu šta provjera dobija i vraća |
| 10 min | Priprema za kontrolnu tačku | Čitaju tekst servisa i povrata robe; pitanja o zahtjevima |
| 5 min | Samoprovjera | Svako sam odgovara na tri pitanja |

Vrijeme je okvirno. Ako tema potraje, skratiti zadatke na času jer su
ionako domaći. Pripremu za kontrolnu tačku ne preskakati: studenti treba da
razumiju zadatke prije nego ih rade kod kuće.

## Samoprovjera na kraju časa

Svako sam, bez gledanja slajdova, za dva do tri minuta:

1. Dobavljač šalje „Potvrdu” ili „Odbijanje”, a rok je dva dana. Koji
   element čeka i zašto ne receive task?
2. Narudžbina ima od jedne do dvadeset stavki. Kako modelujete provjeru
   svake stavke?
3. U petlji dvije strelice ulaze u isti task. Šta mijenjate?

Odgovori: event-based gateway sa dvije poruke i tajmerom, jer receive task
čeka samo jednu vrstu poruke. Jedan task sa multi-instance oznakom, jer
broj stavki ne znamo unaprijed. Ispred taska dodajemo XOR koji spaja obje
strelice.

Ko griješi u prvom pitanju, ponoviti poruke i event-based gateway prije
kontrolne tačke. Ko griješi u drugom ili trećem, uputiti na domaći.

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

Dva zadatka na novim primjerima, ne na nabavci. Ove godine su domaći za
vježbu prije kontrolne tačke.

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
