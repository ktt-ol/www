+++
title = "Flying Games Logo"
description = "USB-Ladegerät fürs Fahrrad"
date = "2012-11-06T23:42:00"
updated = "2024-03-24T23:42:00"
authors = ["fermate"]

[taxonomies]
Serie = ["Projekt"]
Typ = ["Hardware"]

[extra]
thumbnail = "/media/blog/2012/flying-games-logo/thumbnail.jpg"
+++

Seit dem 1.11.12 bin ich Mitglied, und am 3.11. war ich das erste Mal "so
richtig" im Hackspace, der jetzt den schönen Namen "Mainframe" trägt. Ich kam
gerade rechtzeitig zu einem Vortrag der Mainframe-Reihe, über Fourier-Analysen:
war spannend und gut erklärt, und ich konnte meine Mathe-Kenntnisse an einem
praktischen Beispiel - mit Elektronik-Demo! - auffrischen.

Danach fing ich mit meinem ersten kleinen Projekt an. Ich wollte das Logo des
Spiele-Kleinverlags Flying Games aus Styropor ausschneiden, um es dann bei
Spielevorstellungen an einer langen, dünnen Stange über dem Spieltisch
"fliegen" lassen zu können. Das Logo hatte ich von Markus, dem Verleger, als
PDF im Vektorformat bekommen. Im Original sah das so aus:

![](/media/blog/2012/flying-games-logo/0000.jpg)

Das musste ich jetzt in eine SVG-Datei umwandeln, die nur noch einen langen
Pfad enthält. Zunächst verband ich also die Umrisse des Logos (die beiden
Flügel mit der Spieleschachtel in der Mitte) und erhielt das hier:

![](/media/blog/2012/flying-games-logo/0001.jpg)

Die Buchstaben "F" und "G" machten mir etwas Kopfzerbrechen, ich beschloss
schließlich, sie von unten her anzuschneiden und durch die gleiche Öffnung
wieder zurückzukehren zum Umriss. Damit würde das Logo dann zwei schmale Löcher
bekommen, aber die könnte ich hinterher vielleicht wieder kleben. Die Vorlage
sah dann so aus:

![](/media/blog/2012/flying-games-logo/0002.jpg)

Damit ging es dann zum PC, der den Styroschneider steuert. Die SVG-Datei wurde
dort mit Inkscape geöffnet, und das Plugin sollte sie in GCode umwandeln. Damit
wird der Schneider angesteuert - ist auch Thema im nächsten Mainframe-Vortrag.

Zunächst war die generierte Datei aber leer. Ich hatte vergessen, den Pfad auch an einer Stelle zu öffnen, damit der
Styroschneider einen Anfang hat. Außerdem mag das Plugin wohl keine gruppierten Objekte. Auch mit der Skalierung passte
es noch nicht ganz (das Modell war viel zu klein), aber das konnte in Inkscape leicht angepasst werden.

Dann hatten wir gültigen GCode und mussten nur noch den Styroschneider an die richtige Position fahren und ihm sagen, wo
im Koordinatensystem des Objekts er anfangen sollte. Und los gings! Schließlich war das Logo fertig und sah so aus:

![](/media/blog/2012/flying-games-logo/0003.jpg)

Und mit dem Video vom Schnitt habe ich ein weiteres erstes Mal gewagt: mein erstes Youtube-Video.

![](https://www.youtube.com/watch?v=huOZjmjd00w)
