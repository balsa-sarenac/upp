# Pristup nastavi 2026-2027

Radni dokument za nastavnike. Studenti ga ne moraju čitati.

## Studenti i termini

- Master studenti koji dobro programiraju, uglavnom u Javi i C#-u.
- Pet grupa po oko 16 studenata. Tri grupe drži Balša, dvije kolega.
- Oko deset termina po 90 minuta. Rad i provjere su na času.

## Od čega polazimo

Studenti već prave procese kroz kolonu `status`, uslove nad statusom,
cron za rokove, tabelu istorije i email na kraju. Na tom iskustvu
objašnjavamo BPMN i pokazujemo koliko rada traži takvo ručno rješenje.
Kad se uklapa u temu, prvo kratko razgovaramo kako bi proces napravili
u kodu. Kod tada ne pišu.

Na predmetu *Upravljanje poslovnim procesima* tražimo i preciznu notaciju:
ispravne gateway-e, pool-ove i poruke. Programersko iskustvo pomaže da
studenti razumiju model, ali ga ne zamjenjuje.

## Kako vodimo čas

Kad tema dozvoljava, krenemo od kratkog teksta zahtjeva. Parovi pet
minuta razgovaraju o tabelama, stanjima i handler-ima, bez pisanja koda.
Zatim dodajemo rok, restart servera, pitanje gdje je zahtjev #1234 zapeo
ili promjenu pravila dok su instance još aktivne.

Isti proces prikažemo BPMN dijagramom i tražimo da ga studenti pročitaju.
Potom crtaju sami, na papiru ili u Camunda Modeler-u. Na kraju provjerimo
šta model olakšava i u kojim slučajevima se takav pristup ne isplati.
Za novi konstrukt dovoljan je mali primjer prije samostalnog pokušaja;
cijelo rješenje prikazujemo nakon pokušaja i ostavljamo vrijeme za ispravke.

## Veza sa programiranjem

Ovoj tabeli vraćamo se tokom semestra:

| Studenti znaju | BPMN / Camunda |
| --- | --- |
| `if/else`, `switch` | ekskluzivni gateway (XOR) |
| `Task.WhenAll`, `CompletableFuture.allOf` | paralelni gateway (AND) |
| `await` na spoljni događaj | poruka, međudogađaj |
| timeout, zakazani posao | tajmer, boundary tajmer |
| `try/catch` | error boundary događaj |
| saga, kompenzacija | kompenzacija, potproces |
| poziv funkcije | call activity |
| kolona `status` + tabela istorije | instanca procesa + istorija (Operate) |
| worker nad redom poruka | job worker |

## Koristi koje pokazujemo

Argument o zajedničkom jeziku za biznis i IT ostavljamo u pozadini.
Ovoj publici više znače stvari koje može sama provjeriti:

- Proces sačuva stanje i nastavi poslije restarta.
- Rokove i ponavljanja zadajemo tajmerima u modelu umjesto svojim cron poslovima.
- U Operate-u vidimo gdje je instanca stala i zašto.
- Nova verzija modela može raditi uporedo sa već pokrenutim instancama.
- Model određuje šta i kada treba uraditi, a kod kako se pojedinačni posao obavlja.
- Za nepouzdan AI worker proces dodaje validaciju, ljudski pregled, ponavljanja i rezervnu putanju.

## Kada se ne isplati

Studenti treba da znaju i granice pristupa. Kratak sinhroni zahtjev sa
jednim odgovorom, ili jednostavan tok bez čekanja, rokova i više učesnika,
često ne opravdava dodatnu platformu.

Tim može izabrati i da cijeli proces opiše u kodu. Alati kao Temporal
rješavaju trajnost, ali ne daju model koji čitaju i ljudi koji ne
programiraju. Cilj je da studenti svjesno izaberu pristup.

## Teme po sedmicama

| Sedmica | Programerski ugao |
| --- | --- |
| 1 | Reklamacija: diskusija o kodu, novi zahtjevi, model. Vježbe prijave ispita i odbrane rada. |
| 2 | Dva zadatka na istoj nabavci. Mali primjeri, pokušaj A, analiza i ispravka; novi elementi, pokušaj B, analiza i ispravka. Za B ostaviti 20 minuta i ponuditi ispravan A onima kojima treba. Tok izvršavanja pokazati obojenim strelicama, uključujući čekanje na AND spajanju. Završiti greškama i individualnom provjerom rezultata i rokova. Prisjećanje je na početku sljedećeg termina. Event-based gateway i kompenzaciju odlažemo. |
| 3 | Provjera modelovanja i utvrđivanje. Ako ostane vremena, početak rada sa formama i promjenljivama. |
| 4 | Camunda forme i promjenljive. Gdje je sada tabela `status`? |
| 5 | Job worker u Javi ili C#-u, jedan test procesa i kratko poređenje sa code-first pristupom. |
| 6 | AI pomaže pri generisanju i pregledu modela. Njegovo rješenje provjeravamo kao i svako drugo. |
| 7-8 | AI kao nepouzdan worker: validacija, ljudski pregled i obrada neuspjeha. |
| 9-10 | Zaokruživanje rada, provjere i povratne informacije. |

## Pitanja na provjerama

Uz demonstraciju tražiti da student promijeni pravilo dok su instance
u toku, pronađe i riješi incident u Operate-u ili objasni šta bi bilo
poslije restarta usred procesa. Takva pitanja pokazuju koliko razumije
model koji je nacrtao.

## Šta još treba provjeriti

Java ima zvanični Camunda 8 SDK. Za C#, koliko znamo, postoji community
klijent. Prije četvrte sedmice provjeriti i REST API za verziju koju
koristimo.

Docker vjerovatno nije dostupan, pa je Camunda SaaS realna opcija.
Probni period je ograničen. Treba provjeriti ima li Camunda program za
obrazovanje.

Za 16 studenata po pet minuta treba oko 80 od 90 minuta. U trećoj i
petoj sedmici provjera je planirana istog dana kad i nova tema; treba
da se dogovorimo koliko vremena ostaje za nastavu.

Na dijagramu reklamacije (`vjezbe/class1/bpmn.png`) obavještenje postoji samo
na grani "Odbijeno", dok tekst traži obavještenje o oba ishoda. Labele
su latinicom bez dijakritika.
