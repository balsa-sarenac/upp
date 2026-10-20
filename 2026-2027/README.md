# Upravljanje poslovnim procesima

## Vježbe 2026–2027

Vježbe obuhvataju oko deset termina od po 90 minuta. Koristimo platformu
[Camunda 8](https://docs.camunda.io/) i zajednički primjer: zahtjev za
nadoknadu troškova sa priloženim računom. Manje vježbe i implementacije
radimo i ocjenjujemo na času, umjesto velikog projekta za rad kod kuće.

| Sedmica | Tema i rad na času | Provjera |
| --- | --- | --- |
| 1 | BPMN: učesnici, saradnja i tokovi poruka | |
| 2 | Grananja, paralelizam i događaji | |
| 3 | Potprocesi i izuzeci | Kontrolna tačka 1: modelovanje |
| 4 | Camunda: forme, promjenljive i ljudski zadaci | |
| 5 | Servisna integracija i izvršavanje malog procesa | Kontrolna tačka 2: izvršavanje |
| 6 | AI pomoć u razvoju: generisanje i pregled modela, nedostajući zahtjevi i greške | |
| 7 | AI integracija: izdvajanje podataka iz dokumenta ili klasifikacija | |
| 8 | Validacija izlaza, ljudski pregled i obrada neuspjeha | |
| 9 | Zaokruživanje AI integracije | Kontrolna tačka 3: AI integracija |
| 10 | Povratne informacije i preostale provjere | Ponovna provjera znanja |

## Zajednički primjer

Zaposleni podnosi zahtjev sa računom, odgovorna osoba ga odobrava ili
odbija, a servis evidentira odluku i šalje potvrdu. Kasnije dodajemo AI
izdvajanje podataka sa računa; nepotpun ili neispravan rezultat ide na
ljudski pregled.

## Kontrolne tačke

Svaki student dobija individualnu varijaciju primjera (drugi limit
iznosa, dodatno odobrenje ili rok za odgovor), a rješenje kratko
demonstrira i objašnjava na času.

1. **Modelovanje:** BPMN model koji odgovara zahtjevima, sa odlukama,
   sinhronizacijom i obradom izuzetaka.
2. **Izvršavanje:** proces se pokreće, ljudski zadatak se završava, servis
   se poziva, a student objašnjava kako se podaci mijenjaju.
3. **AI integracija:** AI korak, validacija rezultata i tok za ljudski
   pregled ili obradu neuspjeha.

Predaje se model sa datotekama potrebnim za pokretanje, kao i kratka
bilješka o upotrebi AI alata: šta je predloženo, šta je prihvaćeno, a šta
ispravljeno. Raspodjela poena biće objavljena uz kriterijume provjera.

## Materijali

- [Čas 1: Uvod u BPMN](vjezbe/class1.md)

Uputstvo za pristup Camunda 8 okruženju biće objavljeno prije dijela o
izvršavanju procesa. Uputstvo za kompajliranje prezentacija je u
[README-u u korijenu](../README.md).
