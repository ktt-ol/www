+++
title = "Smartphone Debug Adapter"
date = "2013-07-14T23:00:00"
authors = ["sre"]

[taxonomies]
Typ = ["Projekt"]
Serie = ["Hardware"]

[extra]
thumbnail = "/media/blog/2013/smartphone-debug-adapter/thumbnail.jpg"
+++

Dieser Artikel beschreibt den Bau eines Debug-Adapters für das [Nokia
N900](https://en.wikipedia.org/wiki/Nokia_N900) Smartphone. Dieser ermöglicht
den Zugriff auf eine die serielle Schnittstelle, so dass Debug-Ausgaben des
Kernels abgefangen werden können.

Hürden für den Bau eines solchen Adapters stellen hauptsächlich zwei Probleme:

* Die Testpads sind unter dem Akku plaziert
* Die Testpads arbeiten mit einer Spannung von 2.7 Volt

Um einen nicht bootenden Linux-Kernel genauer zu analysieren wird üblicherweise
auf eingebetteten Geräten [JTAG](https://en.wikipedia.org/wiki/JTAG) und/oder
eine serielle Schnittstelle als Debug-Ausgabe verwendet. Auf dem von mir
verwendeten Smartphone von Nokia, dem N900, wird eine solche serielle
Schnittstelle in Form von Testpads herausgeführt. Das Pinout für die serielle
Schnittstelle wurde bereits vor meiner Arbeit von Hackern der
[Maemo](http://maemo.org/)-Gemeinschaft analysiert und dokumentiert ([N900
Debug Ports](http://wiki.maemo.org/N900_Hardware_Hacking#Debug_ports)), so dass
auf vorhandenes Wissen zurückgegriffen werden konnte.

Für den Bau des Adapters habe ich zunächst Federkontaktstifte ([GKS-181 305 080
A 1500 L](http://www.ingun.de/media/pdf/ks/gks_de/gks-181-d.pdf)) besorgt,
welche den eigentlichen Kontakt zum Testpad herstellen sollen. Diese sind z.B.
auf ebay erhältlich.

Als nächstes habe ich das geöffnete Telefon in einen Flachbrettscanner gelegt,
um die Positionen der Testpads zu erhalten. Zusätzlich habe ich die Maße des
Akkufachs mit einer Schieblehre abgemessen, um die Grafik korrekt zu skalieren.

Als nächstes habe ich die Grafik in [Inkscape](http://inkscape.org/) geöffnet
und die wichtigen Strukturen vektorisiert, so dass ich mittels
[CNC](https://en.wikipedia.org/wiki/CNC)-Technik einen eigenen Akku herstellen
kann, der an den Testpads Löcher für die Kontaktstifte hat.

An die Kontaktstifte wurde von mir ein Pegelwandler ([Sparkfun
8745](https://www.sparkfun.com/products/8745)) angeschlossen, welcher das
TTL-Signal von 5V oder 3.3V auf 2.7V wandeln kann.  Dazu benötigt er eine
5V/3.3V Referenzspannung, sowie eine 2.7V Referenzspannung. Hierzu wurde von
mir ein [LM336Z](http://www.linear.com/docs/1818) (von Pollin) verwendet,
welcher aus 5V eine 2.5V Referenzspannung erstellt. Damit kann auf einer Seite
des Pegelwandlers ein normaler 5V USB-TTL-Adapter angeschlossen werden und auf
der anderen Seite der serielle Port des N900.

Zum Schluss habe ich noch ein kleines Gehäuse für den Akku designt, damit
dieser einfach mit dem Debug-Adapter verbunden werden kann.

-- Sebastian

Einzelteile:
![Einzelteile](/media/blog/2013/smartphone-debug-adapter/0001.jpg)

Elektronik:
![Elektronik](/media/blog/2013/smartphone-debug-adapter/0002.jpg)

Adapter:
![Adapter](/media/blog/2013/smartphone-debug-adapter/0003.jpg)
