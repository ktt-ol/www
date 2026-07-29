+++
title = "Projekt: Beispiele für Infill im 3D-Druck"
date = "2026-07-29T19:42:00"
updated = "2026-07-29T19:42:00"
authors = ["tljuniper"]
description = 'Um zu zeigen, was im 3D-Druck mit "Infill" gemeint ist und welche Arten dieser Füllstruktur es gibt, haben wir ein Sample-Brett mit Beispielen gedruckt.'

[taxonomies]
Serie = ["3D-Druck"]
Typ = ["Projekt"]

[extra]
thumbnail = "/media/blog/2026/infill-samples/thumb.jpg"
+++

Im 3D-Labor haben wir ein neues Beispiel und Anschauungsobjekt hinzugefügt: Ein Brett mit verschiedenen Infill-Samples.

Infill ist die Füllstruktur im Inneren eines 3D-gedruckten Teils. In den meisten
Fällen werden Objekte im 3D-Druck nicht massiv gedruckt, sondern mit einem
speziellen Muster gefüllt, um Material, Zeit und Gewicht zu sparen. Die Muster
unterscheiden sich in ihrer Stabilität, Druckgeschwindigkeit und natürlich der
Optik. Das Konzept kennt man auch von günstigen Möbeln, die nicht aus Massivholz
bestehen, sondern ebenfalls mit einem Wabenmuster gefüllt sind.

Es sind im 3D-Druck verschiedenste Infill-Muster möglich -- von quadratischen
Gittern über Spiralen, Bienenwaben oder Dreiecken.

## Modell und Konstruktion

Für unser Beispiel-Board haben wir das "Hex infill and surface sample holder wall art" von "The Redcoat"
auf [printables.com](https://www.printables.com/model/200756-hex-infill-and-surface-sample-holder-wall-art) heruntergeladen.
Da es sich um ein OpenSCAD-Modell handelt, konnten wir die Größe der einzelnen
Samples anpassen. Wir haben uns dafür entschieden, die Höhe auf 10mm zu erhöhen,
um mehr vom Infill zu zeigen.

![Infill-Sample Board Close-Up](../../../media/blog/2026/infill-samples/IMG_1875.jpg)

Das Board ist als Wandbild konzipiert und besteht aus drei zusammensteckbaren
Haltern, in die die einzelnen Sechsecke eingesetzt werden können.
Um alle Teile besser zu befestigen, haben wir eine Rückseite aus 8mm starkem Pappelsperrholz gelasert.

![Infill-Sample Board Seitenansicht](../../../media/blog/2026/infill-samples/IMG_1874.jpg)


## Liste der Samples nach Farben

Hier die vollständige Liste der Samples in unserem Beispiel-Board. Wenn nicht anders angegeben, handelt es sich um 15% Infill.

* Orange
    - Archimedan Chords
    - Lightning (Blitze)
* Hellblau
    - 2D lattice
    - Support Cubic
* Transparent Blau
    - Hilbert Curve
    - Gyroid
    - Octagram Spiral
    - Cubic
* Pink
    - 3D Honeycomb
    - Rectlinear Aligned
* Braun
    - Crosshatch
    - Zigzag
* Dunkelgrün
    - Cross Zag
    - Locked Zag
* Hellgrün
    - Rectlinear
    - Concentric
* Transparent Farblos
    * Gyroid 5%
* Dunkellila/Beere
    - Grid
    - Line
    - Triangles
* Rot
    - Archimedan Chords
    - 3D Honeycomb
* Gelb
    - Honeycomb
    - Tri-hexagon
* Weiß
    - Lightning 30%
    - Honeycomb 5%
* Blau (hier wird die oberste Schicht und nicht der Infill gezeigt)
    - Rectlinear (top layer)
    - Concentric (top layer)

![Infill-Sample Board](../../../media/blog/2026/infill-samples/IMG_1871.jpg)
