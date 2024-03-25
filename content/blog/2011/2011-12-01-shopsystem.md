+++
title = "Shopsystem"
description = "USB-Ladegerät fürs Fahrrad"
date = "2011-12-01T10:00:00"
updated = "2024-03-24T23:42:00"
authors = ["sre", "lhw"]

[taxonomies]
Serie = ["Projekt"]
Typ = ["Software"]

[extra]
thumbnail = "/media/blog/2011/shopsystem/shopsystem.jpg"
repository = "https://github.com/ktt-ol/serial-barcode-scanner/"
+++

![](/media/blog/2011/shopsystem/shopsystem.jpg)

Mit steigender Mitgliederzahl und mehr als 5 verschiedenen Produkten im "Kiosk"des Hackspaces wurde das führen und
auswerten von Strichlisten immer aufwändiger. Aus diesem Grund wurde von uns Software entwickelt, welche die Daten von
Beginn an digital vorhält.

Das Shopsystem läuft auf einem Raspberry Pi, an welchen ein serieller Barcode Scanner angeschlossen ist. Des Weiteren
ist an den Raspberry Pi ein Monitor angeschlossen, welcher die letzten Vorgänge protokolliert. Jedes Mitglied kann sich
mit einem (ungeschützten und leicht fälschbaren) Barcode einloggen, dann beliebige Produkte kaufen, indem er deren EAN
Barcode scannt und sich schließlich mittels eines logout barcodes ausloggen. Um zu verhindern, dass Personen den Barcode
anderer Mitglieder scannen bekommen diese gegen 8 Uhr eine E-Mail, in der die eingekauften Produkte des Vortages
aufgelistet sind. Am Anfang des folgenden Monats kommt dann, ebenfalls per E-Mail, die Rechnung für den gesamten Monat.
Diese wird, zusammen mit einer einfach auswertbaren CSV-Datei auch an den Schatzmeister geschickt, welcher dann das Geld
von den Mitglieder Konten einzieht.

Das Eintragen neuer Produkte geschieht über ein Web-Interface. Über dieses kann auch die Mitgliederdatenbank des Systems
aktualisiert werden (import einer CSV-Datei) oder der aktuelle Warenbestand eingesehen werden.
