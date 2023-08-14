# 📷 QR-Code Scanner

Der Scanner ließt und verifiziert die vom Generator erstellten QR-Codes.

## ⚡ Qick Start
1. Starte das Programm *ACR_QR_Scanner.exe*
2. Gib den Veranstaltungsnamen und das Veranstaltungsdatum ein und bestätige mit *Ok*.
3. Beim ersten Starten muss die public key Datei des Generators über das Menü *Datei > Wähle Key Datei* ausgewählt werden. Beim Neustart des Programms wird die Datei dann automatisch wieder ausgewählt.
4. Scanne QR-Codes. Ein grüner Rahmen bedeutet der QR-Code wurde erfolgreich gescannt. Ein roter Rahmen bedeutet, dass ein Fehler aufgetreten ist. In dem Fall wird zusätzlich eine Meldung angezeit die den Fehler beschreibt.

## ⚙ Konfiguration
Jeder erfolgreich gescannte QR-Code wird zu Nachverfolgungszwecken in einer Logdatei protokolliert. Jeder Eintrag in dieser Datei besteht aus einem Zeitstempel und der ID des QR-Codes.

> **_⚠️_** Der Zeitstempel ist in UTC Zeit. Das sorgt für eine Stunde Verschiebung zur mitteleuropäischen Zeit (MEZ) und zwei Stunden Verschiebung zur mitteleuropäischen Sommerzeit (MESZ).

Der Speicherort der Logdateien kann über das Menü *Datei > Ausgabeordner wählen* geändert werden. Diese Einstellung bleibt nach Neustart des Programms bestehen.

> **_⚠️_** Ändere diese Einstellung nicht während einer Veranstaltung.

Über das Menü *Konfiguration > Kamera ändern* kann im Fall von mehreren verfügbaren Kameras die verwendete Kamera geändert werden. Das Ändern der Kamera kann einen Moment dauern.

## 🔍 Details

* Veranstaltungsname und Veranstaltungsdatum müssen exakt den Einstellungen entsprechen mit denen die QR-Codes generiert wurden
* Sollte sich das Veranstaltungsdatum geändert haben, muss das ursprüngliche Datum verwendet werden.
* Sollte während einer Veranstaltung der Scanner neu gestartet werden, dann werden die bereits gescannten QR-Codes aus der Logdatei wiederhergestellt. Daher sollte vermieden werden den Ausgabeordner der Logdatei während einer Veranstaltung zu ändern. Sonst kann nicht mehr sichergestellt werden, dass QR-Codes nicht mehrfach von verschiedenen Personen verwendet werden.