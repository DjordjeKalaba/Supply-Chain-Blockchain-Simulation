**Supply Chain Blockchain Simulation**

Ovaj projekat predstavlja simulaciju lanca snabdijevanja implementiranu korišćenjem blockchain strukture podataka. Aplikacija omogućava praćenje proizvoda kroz više faza isporuke, od proizvođača do krajnjeg kupca, uz osiguranje integriteta podataka i transparentno praćenje svake promjene.

GUI aplikacija je razvijena u Python-u koristeći Tkinter, dok je sama blockchain logika implementirana kao lokalni, samostalni modul unutar aplikacije.

**Opis sistema**

Svaki proizvod se tretira kao zaseban blockchain lanac. Prvi blok (genesis blok) se automatski kreira, a zatim se dodaju novi blokovi koji predstavljaju faze u lancu snabdijevanja:
Manufacturer(proizvođač)
Distributor(distribucija)
Retailer(prodavnica)
Customer(kupac)

Svaki blok sadrži:
Naziv proizvoda
Fazu u lancu snabdijevanja
Entitet koji je obradio proizvod
Status uspješnosti
Vremensku oznaku
Hash i prethodni hash (za validaciju integriteta)

**Funkcionalnosti**

Kreiranje novih proizvoda i inicijalizacija blockchaina
Obrada proizvoda kroz definisane faze lanca snabdijevanja
Validacija redoslijeda faza (strogo kontrolisan workflow)
Verifikacija integriteta blockchaina
Detekcija korupcije podataka (hash mismatch / chain break)
Pregled kompletne istorije proizvoda
Grafički prikaz statusa proizvoda kroz faze
Vizuelni dashboard svih proizvoda
Perzistentno čuvanje podataka u JSON fajlu

**Tehnologije**

Python
Tkinter (GUI)
SHA-256 hashing
JSON storage
Objektno orijentisano programiranje
