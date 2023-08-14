# 🏭 QR-Code Generator

Der Generator erstellt QR-Codes die als E-Tickets für Veranstaltungen genutzt werden können.

## ⚡ Quick Start

1. Starte das Programm *ACR_QR_Generator.exe*
2. Klicke den *Neu generieren* Button in der geöffneten Infobox
3. Lege den Namen der Veranstaltung, das Datum* und die Anzahl der gewünschten QR-Codes fest
4. Drücke den *Start* Button um die Generierung zu starten
5. Wenn die Generierung abgeschlossen ist kann der Ausgabeornder über die Infobox geöffnet werden

\* Sollte die Veranstaltung auf ein anderes Datum verschoben werden ist dies nicht weiter schlimm. Es muss dann im Scanner lediglich das ursprüngliche Veranstaltungsdatum konfiguriert werden. 

## ⚙ Konfiguration

Über das Menü *Datei > Ausgabeordner wählen* kann der Ausgabeordner in den die QR-Codes generiert werden verändert werden. Änderungen des Ausgabeordners bleiben nach Neustart des Programms bestehen.

## 🔐 Sicherheit

> **_⚠️_** Bitte ließ diesen Abschnitt gründlich um zu verhindern, dass Tickets gefälscht werden können

Beim erstmaligen Starten des Generators wird ein asymetrisches Schlüsselpaar erstellt. Dieses besteht aus einem privaten Schlüssel (private key) und einem öffentlichen Schlüssel (public key).

Der private key wird vom Generator genutzt um die QR-Codes digital zu signieren. Wenn das Programm neu gestartet wird, wird der bereits generierte private key wieder verwendet. Der public key hingegen wird vom Scanner genutzt um die Signatur zu verifizieren. Dieses Vorgehen stellt sicher, dass niemand, der nicht im Besitz des private keys ist, in der Lage ist gefälschte QR-Codes zu generieren. Der Ordner mit den generieren Schlüsseln kann über das Menü *Datei > Key Ordner öffnen* geöffnet werden.

> **_⚠️_** Stelle sicher, dass niemand unbefugtes Zugang zu dem private key erlangt. Z.B. indem du ihn auf einem Gerät speicherst zu dem nur ausgewählte Personen Zugang haben oder indem du ihn durch ein Passwort sicherst.

Solltest du den private key an einem anderen Ort speichern wollen als der Standardordner ist dies möglich. Verschiebe dazu den private key einfach an den gewünschten Ort und wähle beim Start des Programms in der Infobox den *Importieren* Button um dem Programm mitzuteilen wo der private key sich befindet. Der festgelegt Ort wird bei Neustart des Programms wieder verwendet.

Wie bereits oben erwähnt wird der public key vom Scanner benutzt um die Signatur in den QR-Codes zu überprüfen. Der public key muss dazu manuell auf das Gerät mit dem Scanner transferiert werden. Dieser Transfer ist, sofern sich der private key nicht ändert, nur einmal notwendig. Es macht also Sinn, den private key nicht unnötig neu zu generieren um nicht ständig den public key auf das Scanner Gerät transferieren zu müssen. Für den public key sind keine besonderen Schutzmaßnahmen notwendig. Er kann also bedenkenlos verteilt werden. 