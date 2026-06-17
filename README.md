**Supply Chain Blockchain Simulation**

Ovaj projekat predstavlja simulaciju lanca snabdijevanja zasnovanu na konceptu blockchain tehnologije. Cilj sistema je praćenje proizvoda kroz različite faze isporuke, od proizvođača do krajnjeg kupca, uz osiguranje integriteta i transparentnosti podataka.

Aplikacija je razvijena kao jednostavna GUI desktop aplikacija koja omogućava unos, pregled i verifikaciju podataka o kretanju proizvoda kroz lanac snabdijevanja.

**Opis sistema**

Svaki proizvod prolazi kroz više definisanih entiteta u lancu snabdijevanja, kao što su proizvođač, distributer, prodavnica i kupac. Svaka faza se bilježi kao blok u blockchain strukturi, gdje svaki blok sadrži informacije o obrađivaču, vremenu obrade i statusu isporuke.

Korisnici mogu pratiti kompletan put proizvoda, pregledati istoriju svih faza i provjeriti integritet blockchaina kako bi se osiguralo da podaci nisu mijenjani.

**Funkcionalnosti**

Unos podataka o fazama lanca snabdijevanja
Evidencija obrade proizvoda kroz različite entitete
Praćenje trenutnog statusa proizvoda
Pregled kompletne istorije kretanja proizvoda
Verifikacija integriteta blockchain strukture
Simulacija kretanja više proizvoda kroz lanac snabdijevanja
Grafički prikaz statusa i istorije proizvoda kroz GUI

**Arhitektura sistema**

Sistem je implementiran korišćenjem jednostavne blockchain strukture gdje je svaki blok povezan sa prethodnim putem hash vrijednosti, čime se osigurava nepromjenjivost podataka. GUI aplikacija omogućava korisnicima interakciju sa sistemom i vizuelni prikaz procesa.

**Tehnologije**

GUI desktop aplikacija (WPF)
Objektno orijentisano programiranje
Blockchain koncept (hash povezani blokovi)
Lokalna simulacija podataka
