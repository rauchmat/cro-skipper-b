# Adria · Cro Skipper B

Mobile-first, frameworkfreie Progressive Web App zum Lernen für das kroatische Küstenpatent. Android/Chrome und iPhone/Safari, ohne App Store.

## Enthalten

- 308 eigenständig formulierte Fragen in 15 Themenbereichen
- 97 Single-Choice-Fragen und 16 schematische Bildaufgaben
- Schnellrunden, thematisch gemischte Testprüfungen (10/20/30 Fragen), Themenlernen, Fehlerwiederholung, mündliche und Partnerprüfung
- Offene Antworten im Prüfungsmodus: Eingabe, Auflösung erst nach Abgabe, anschließend Selbstbewertung
- Lokaler Lernstand, Wiederholungsintervalle, Fortsetzen einer Runde, JSON-Export/-Import
- Manifest, App-Icons und Service Worker mit vollständig vorab geladenem Inhalt
- Keine externe Schrift, Tracking-Bibliothek, API oder Datenbank erforderlich

## Lokal starten

```sh
python3 -m http.server 8080 --directory dist
```

Dann `http://localhost:8080` öffnen. Für Service Worker braucht es HTTPS oder localhost. Auf dem Handy ist eine HTTPS-Veröffentlichung erforderlich.

## Inhalte bearbeiten

`bank.txt` enthält die redaktionellen Kernfragen: Thema als `@Thema`, dann je Zeile `Seite|Frage|Antwort|Erklärung|drei falsche Antworten mit Semikolon` (letztes Feld optional).

`build_bank.py` ergänzt Funkalphabet, Abkürzungen, Begriffe, Bildaufgaben, Quellen und Korrekturhinweise. Stabile Frage-IDs werden aus dem Fragetext abgeleitet. Eine Änderung des Fragetextes erzeugt eine neue ID; der bisherige Lernstand dieser Frage wird nicht automatisch übertragen.

```sh
python3 build_bank.py
python3 build_pwa.py
node tests/validate.mjs
```

Für `build_pwa.py` wird Pillow benötigt (`python3 -m pip install Pillow`). Die ausgelieferte App selbst hat keine Abhängigkeiten. **Nach jeder Änderung an `dist/` zuletzt `build_pwa.py` ausführen**, damit die Offline-Version aktualisiert wird. `dist/` wird bewusst mit versioniert und kann unverändert auf einem statischen HTTPS-Host ausgeliefert werden. Unterverzeichnisse wie GitHub Pages werden durch relative URLs unterstützt.

## Speicherung

Lernstände liegen im Browser in `localStorage` unter `adria-progress-v1`. Keine Synchronisierung zwischen Geräten. Der Service Worker speichert ausschließlich den App-Inhalt; externe Quellen werden nicht gecacht. Löschen der Browser-/Website-Daten kann Fortschritt und Offline-Inhalt entfernen. Safari und eine installierte Home-Screen-App können unterschiedliche Speicher verwenden. Der Export sichert abgeschlossene Lernstände, nicht eine laufende Runde.

Offline-Nutzung nach dem ersten vollständigen Laden möglich, sobald „Offline bereit“ angezeigt wird. Bei Veröffentlichung hinter einer Zugangskontrolle kann eine Anmeldung nötig sein. Ein kopierter Link allein erteilt keine Zugriffsrechte.

## Fachliche Grundlage

Grundlage: [AC Nautik Boat Skipper B Skriptum](https://www.kuestenpatent-kroatien.at/Skriptum.pdf), Lernkapitel S. 5–59 und Beispielfragen S. 60–64. Das Original-PDF und dessen Illustrationen werden **nicht** mitverteilt. Bilder sind eigene schematische Signaldiagramme. Werbung, Anfahrt und Kursangebote wurden nicht in den Lernkatalog aufgenommen.

Erkannte Fehler oder Verkürzungen wurden anhand offizieller Quellen präzisiert. Besonders relevant: optionale Segler-Zusatzlichter, Lotsenlichter, Glocke ab 20 m, kein allgemeiner Fährenvorrang, DSC-Begriff und kroatische Küsten-/Badebereichsabstände nach NN 52/2025 und NN 40/2026. Quellenlinks und Hinweise stehen direkt an den Fragen. Prüfung ausgewählter Änderungen: 11.09.2026.

Kein amtlicher Fragenkatalog und keine vollständige aktuelle Rechts-/Ausrüstungsberatung. Historische Ausrüstungstabellen sind ausdrücklich als Skript-Lernstoff markiert. Lokale Funkkanäle, Einreiseverfahren und Gebühren nicht ungeprüft verwenden. Keine offizielle Bestehensgrenze. Praktische Kartenarbeit und Knoten müssen zusätzlich am Material und mit qualifizierter Kontrolle geübt werden.

## Validierung

`tests/validate.mjs` prüft Katalogkonsistenz, lokale Asset-Verweise, thematische Verteilung, keine doppelten Fragen in Runden, Schutz gegen doppelte Bewertungen, Datenimport und Prüfungsabläufe inklusive verdeckter Lösungen. Es ist ein Node-basierter Zustands-/DOM-Harness, kein echter Browsertest. Installation, Offline-Betrieb und Darstellung auf realem iPhone/Android müssen dort zusätzlich überprüft werden. Optionales WebMCP ist feature-detected; eine unterstützte Browserumgebung war bei Erstellung nicht verfügbar.

## Veröffentlichung

Alle öffentlichen Dateien liegen in `dist/`. Die Datei `.openai/hosting.json` gehört zur registrierten Sites-Veröffentlichung. Sie enthält keine Zugangsdaten. Keine Tokens oder Lernstände gehören ins Repository.
