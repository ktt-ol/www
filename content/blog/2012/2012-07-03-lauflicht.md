+++
title = "Lauflicht"
description = ""
date = "2012-07-03T12:15:00"
updated = "2024-03-24T23:42:00"
authors = ["MarvinGS"]

[taxonomies]
type = ["Projekt", "Hardware"]

[extra]
thumbnail = "/media/blog/2012/lauflicht/img1.jpg"
+++

Manchmal fällt uns ein Projekt auch einfach in den Schoß. So wie dieses
Lauflicht aus 192 × 14 LEDs. Das Gerät gehört einem Freund des Vereins, der aber
gerade wenig Zeit und Muße hat, sich der Herausforderung zu stellen, das gute
Stück zu programmieren und somit wieder nutzbar zu machen. Denn dummer Weise
fehlt die zur Programmierung notwendige proprietäre Tastatur zu diesem über 30
Jahre alten Schätzchen. Also hat er es uns in der Hoffnung vorbeigebracht, dass
sich bei uns jemand finden würde, der Lust auf diese Herausforderung hat.

![](/media/blog/2012/lauflicht/img1.jpg)

Hardware die nicht funktioniert oder von der niemand weiß wie sie funktioniert
und dann auch noch mit blinkenden LEDs.

##### CHALLENGE ACCEPTED!

Diesmal wurden unsere Spezialexperten für alte Hardware schwer gefordert. Es
gab keine Handbücher und auch das vorhandene Typenschild verriet uns nur, dass
die Hardware das letzte Mal 1985 gewartet wurde. Es musste also alles selbst
herausgefunden werden. Gesagt, getan. Das Gehäuse wurde aufgeschraubt, der
Controller teilweise ausgebaut mit einem Logic Analyser verbunden und die
zuletzt einprogrammierte Animation durchlaufen gelassen. Der Logic Analyser
hat dabei die Signale aufgezeichnet, die an den Controller geschickt wurden.
Dadurch war es möglich, die einzelnen Kommandos nachträglich genau auszuwerten.
Leider ist es natürlich nicht so, dass einem die Geräte sagen, was warum wann
gerade getan wird. Also starrt man manchmal mehrere Stunden auf solche Kurven
wie in dem Bild.

![](/media/blog/2012/lauflicht/img2.jpg)

Man überlegt, warum gerade an dieser Stelle jetzt gerade Strom an oder aus
gestellt wird, verrennt sich von einer in die nächste Theorie, weiß irgendwann
nicht mehr, warum man die letzte wieder verworfen hat. Schließlich kommt man
auf die selbe Idee zwei oder drei mal und ist am Ende soweit für den Tag
Schluss zu machen, um es am nächsten Tag erneut zu probieren.

Und an dieser Stelle hat sich das Konzept Hackerspace voll ausgezahlt; es
passierte, was passieren soll: Jemand, der bisher völlig unbeteiligt war, lief
vorbei warf einen kurzen Blick auf den Bildschirm sagt etwas wie “Sieht für
mich aus wie eine Binäradressierung”. “HEUREKA!” genau das war’s. Jede LED der
ersten Spalte wird mit einer Zahl zwischen 0 und 13 in Binärdarstellung
angesprochen, dann wird sie entweder auf an oder aus gestellt und, wenn man
damit fertig ist, werden alle Spalten eins weiter geschoben. Danach wird die
neue letzte Spalte bearbeitet. Dies geschieht so schnell, dass es am Ende wie
eine flüssige Animation aussieht. Mittlerweile können wir also unsere eigenen
Animationen abspielen. Und wie üblich, wenn wir sich bewegende LEDs haben,
wollen wir auch damit spielen: Der nächste Schritt ist also die Implementierung
eines Jump-and-Runs à la Super Mario auf 192×14 LEDs. Mal gucken wie schnell
das fertig ist. Und wenn wir spielen können, freuen wir uns natürlich über neue
Gegner, die versuchen, unsere High-Scores zu knacken.

[Video](https://youtube.com/watch?v=Ilu1I9LmIsU)
