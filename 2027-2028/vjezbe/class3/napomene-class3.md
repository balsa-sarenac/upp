# Treći čas: BPMN, nastavak

Svaka tema ide istim redom: pandan u kodu, mali primjer novog elementa,
zadatak, rješenje i pitanja. Petlja i call activity su na 2. času, pa
ovdje ostaju samo teme koje traže poruke ili listu. Tako druga polovina
časa ostaje za kontrolnu tačku.

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

## Plan časa

| Okvirno | Dio časa | Šta rade studenti |
| --- | --- | --- |
| 5 min | Prethodni čas: rješenje B | Prate jedan scenario na rješenju B |
| 15 min | Poruke | Čitaju primjer upita za cijenu, crtaju narudžbinu dobavljaču |
| 10 min | Event-based gateway | Crtaju potvrdu, odbijanje i rok |
| 10 min | Multi-instance | Kažu zašto AND ne radi za listu, crtaju provjeru stavki |
| 5 min | Samoprovjera | Svako sam odgovara na tri pitanja |
| 45 min | Kontrolna tačka 1 | Svako sam: zadatak 1 crta, zadatak 2 opisuje |

Vrijeme je okvirno. Ako tema potraje, skratiti zadatak na času, a ne
kontrolnu tačku.

## Samoprovjera na kraju časa

Svako sam, bez gledanja slajdova, za dva do tri minuta:

1. Dobavljač šalje „Potvrdu” ili „Odbijanje”, a rok je dva dana. Koji
   element čeka i zašto ne receive task?
2. Narudžbina ima od jedne do dvadeset stavki. Kako modelujete provjeru
   svake stavke?
3. Nabavka čeka odgovore za više narudžbina. Kako odgovor stiže pravoj?

Odgovori: event-based gateway sa dvije poruke i tajmerom, jer receive task
čeka samo jednu vrstu poruke. Jedan task sa multi-instance oznakom, jer
broj stavki ne znamo unaprijed. Po broju narudžbine koji poruka nosi.

Ko griješi u prvom pitanju, ponoviti poruke i event-based gateway prije
kontrolne tačke. Ko griješi u drugom ili trećem, kratko pokazati rješenje
na slajdu.

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

### Multi-instance

- **Možemo li nacrtati AND sa granama za svaku stavku?** Ne. AND traži da
  svaku granu nacrtamo, a broj stavki ne znamo dok proces ne krene.

## Kontrolna tačka 1

Dva zadatka na novim primjerima, ne na nabavci. Svako radi sam, na času.

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

### Zadatak 2: odgovor

Služba prima zahtjev. Ako je prošlo više od 14 dana, šalje odbijanje.
Inače šalje uputstvo za slanje. Magacin čeka paket, pa pregleda artikal
po artikal. Za oštećenu robu služba dogovara rješenje sa kupcem. Inače
se paralelno vraćaju novac i artikli na stanje.
