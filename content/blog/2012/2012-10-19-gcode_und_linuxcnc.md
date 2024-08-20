+++
title = "Einführung in GCode und LinuxCNC"
description = "Vortrag über die CNC-Maschinen-Sprache GCode anhand der Software LinuxCNC."
date = "2012-10-19T20:00:00"
updated = "2024-03-24T23:42:00"
authors = ["0xFF"]

[taxonomies]
Typ = ["Talk"]

[extra]
thumbnail = "/media/blog/2012/talk-0002/thumbnail.png"
+++

[![](/media/blog/2012/talk-0002/cover.png)](https://youtube.com/watch?v=go-i1ZhocUQ)

# [Slides](/media/blog/2012/talk-0002/GCode.pdf)

GCode ist die Sprache mit der viele CNC-Maschinen angesteuert werden. Auch wenn
es als Programmiersprache den Charme der 70er versprüht und darauf optimiert
ist, notfalls auf Rechnern mit nur ein paar Byte RAM und ein paar kB
Code-Segment zu laufen, so ist es doch immer noch ein Standard, der auch bei
den 3D-Druckern noch Anwendung findet. Mit LinuxCNC steht auch eine freie
Implementierung zur Verfügung, die auch komplexere Features beherrscht und für
große CNC-Maschinen geeignet ist. Anhand des LinuxCNC GCode-Dialekts werden
die wichtigsten Features der Sprache vorgestellt:

 * Steuerung der Achsen, Werkzeuge und Hilfsaggregate
 * Einstellung von Werkzeugparametern
 * Arbeiten mit Koordinatensystemen
 * Schleifen, Funktionen und Variable
 * Spezialbefehle wie z.B. verschiedene Bohr-Programme

Anschliessend solltet ihr in der Lage sein eine CNC-Maschine per
GCode-Kommandozeile zu bedienen, kleine GCode-Programme selbst zu schreiben
oder aber inkompatiblen GCode auf einen speziellen GCode Interpreter
anzupassen.
