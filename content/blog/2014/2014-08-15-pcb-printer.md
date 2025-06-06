+++
title = "Platinendrucker"
date = "2014-08-15T17:00:00"
authors = ["Hauke"]

[taxonomies]
Serie = ["Projekt"]
Typ = ["Hardware"]

[extra]
thumbnail = "/media/blog/2014/pcb-printer/thumbnail.jpg"
+++

## Platinendrucker/PCB-Printer mit modifiziertem Inkjet-Drucker

Platinen werden üblicherweise aus einer, mit Fotolack und Kupfer beschichteten Trägerplatte, hergestellt.

Es sind dann folgende Arbeitsschritte nötig:

* Layout drucken
* Platine belichten
* Platine entwickeln
* Platine ätzen
* ... (bohren etc)

Mit einem modifizierten Inkjet-Drucker ist es möglich das Layout direkt als
ätzbeständige Farbschicht auf einer, nur mit Kupfer beschichteten Trägerplatte,
aufzubringen. Danach kann die Platine direkt geätzt werden.[1]

Man spart sich also zwei Arbeitsschritte (2 & 3) und eine Chemikalie
(Entwickler).

Erfolgreiche Umbauten eines Epson C84 bzw.  C87 für solche Zwecke kursieren
schon seit ein paar Jahren im Netz [2]. Dieser Drucker besitzt einen
keramischen Piezo Permanent-Druckkopf.

Es muss zuerst der Drucker auseinandergebaut und die Schiene auf der der
Druckkopf sich bewegt angehoben werden, da wir ja in Zukunft nicht mehr auf
dünnem Papier drucken wollen sondern auf Platinenmaterial. Hierzu muss das
Metallchassis an einer Stelle durchgesägt und dann höhergelegt und wieder
fixiert werden (siehe Abbildung). Auf der rechten Seite des Druckes sorgen
Unterlegscheiben für den nötigen Abstand. Auch ist es wichtig die „Parkstation“
für den Druckkopf auf der linken Seite anzuheben, damit dieser nicht
ausstrocknet!

![Drucker](/media/blog/2014/pcb-printer/0000.jpg)

Da das Platinenmaterial auf noch wesentlich unflexibler als Papier ist muss der
Papiereinzug entsprechend so umgebaut werden, dass das Material horizontal
durchgeführt werden kann und auch geführt wird.

![Drucker von oben](/media/blog/2014/pcb-printer/0001.jpg)

Die Hauptarbeit war das Testen unterschiedlicher Parameter wie der Erwärmung
vor und nach dem Drucken auf das Platinenmaterial, Ätzmittel und der Tinte.
Hier lagen auch die Hauptprobleme vieler Nutzer im Netz. Bei den
Standard-Tinten konnten hauptsächlich nur Eisen(III)Chlorid verwendet werden.

Eines Tages und nach vielen Gesprächen später nahm ich allen Mut zusammen und
versuchte es mit Edding(r)-Nachfülltinte aus dem Schreibwarenhandel. Diese
Tinten gelten allgemein als ätzresistent und werde auch zur Nacharbeitung von
Platinen vor dem Ätzen eingesetzt. Es funktionierte tatsächlich (siehe folgende
Abbildungen).

So sieht die Platine nach dem Druck aus:

![Platine nach dem Druck](/media/blog/2014/pcb-printer/0002.jpg)

Nach dem Ätzen (Beispiel für eine SDR-Platine von DD7LP):

![Platine nach dem Druck 2](/media/blog/2014/pcb-printer/0003.jpg)

Vorteil bei Verwendung besagter Tinte ist auch, das als Ätzmittel auch
Natriumpersulfat verwendet werden.

Wichtig ist die Druckköpfe vor einer längeren nicht benutzung mit einer
Patronen mit Isopropanol zu spülen, damit die Tinte in dem Druckkopf nicht
eintrocknen kann. Generell sind nachfüllbare Tintenpatronen mit Auto-Reset Chip
zu empfehlen.

[1] [http://techref.massmind.org/techref/pcb/etch/directinkjetresist.htm](http://techref.massmind.org/techref/pcb/etch/directinkjetresist.htm)

[2] [http://www.cnczone.com/forums/general-cnc-machine-related-electronics/30951-hacking-printer-directly-print-pcbs.html](http://www.cnczone.com/forums/general-cnc-machine-related-electronics/30951-hacking-printer-directly-print-pcbs.html)
