# Generator

Der Generator dient dazu QR Codes für E-Tickets einer Veranstaltung zu erstellen.

## Quick start

1. Öffne *ACR_QR_Generator.exe*
2. Gib im Feld *Veranstaltungsname* den Namen für die bevorstehende Veranstaltung ein. 
3. Gib im Feld *Anzahl QR-Codes* die gewünschte Anzahl der zu generierenden QR-Codes ein.
4. Drücke den *Start* Knopf um die Generierung zu starten
5. Nachdem die Generierung beendet ist kann der Ausgabeordner über das aufgepopte Informationsfenster geöffnet werden

## Konfiguration

Der Ausgabeordner für die generieren QR-Codes kann über das Menü *Datei > Ausgabeordner wählen* geändert werden.

## Sicherheit


Beim erstmaligen Öffnen des Generators wird ein Schlüsselpaar erstellt. Dieses besteht aus einem öffentlichen (public) und einem privaten (private) Schlüssel. Der private Schlüssel dient dazu, die generierten QR Codes digital zu signieren. Mit dem öffentlichen Schlüssel können die Signaturen des privaten Schlüsseln verifiziert werden. Der Speicherort des Schlüsselpaars kann über die Menüleiste *Datei > Key Ordner Öffnen* geöffnet werden.

---
⚠️  Der private Schlüssel muss sicher aufbewahrt werden. Jede Person die Zugriff auf diesen Schlüssel erlangt ist in der Lage QR Codes zu signieren und kann somit potentiell gefälschte E-Tickets erstellen.

---
