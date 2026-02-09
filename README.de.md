# 🕰️ Digital Pendulum

Ein sprechendes digitales Pendel für Home Assistant  
<br>**Autor:** Egidio Ziggiotto (Dregi56)  E-Mail: [dregi@cyberservices.com](mailto:dregi@cyberservices.com)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/Dregi56/digital_pendulum)](https://github.com/Dregi56/digital_pendulum/releases)
![License](https://img.shields.io/github/license/Dregi56/digital_pendulum)
[![GitHub stars](https://img.shields.io/github/stars/Dregi56/digital_pendulum?style=social)](https://github.com/Dregi56/digital_pendulum)

🌍 Verfügbare Sprachen:
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) 
<br>👉Dies ist die italienische README. Verwenden Sie oben die Sprachauswahl


## ❤️ Gefällt dir Digital Pendulum?

Wenn du es nützlich findest, hinterlasse bitte einen ⭐ auf GitHub:  
👉 **https://github.com/Dregi56/digital_pendulum**
<br>Danke.

## 📌 Beschreibung

Digital Pendulum ist eine benutzerdefinierte Integration für Home Assistant, die die Uhrzeit per Sprache ankündigt – wie ein digitales Pendel 🕰️.


Mit einem Alexa-Gerät als Lautsprecher:

- 📢 kündigt die Uhrzeit jede Stunde und/oder jede halbe Stunde an (konfigurierbar)
- 🌍 spricht automatisch in der in Home Assistant eingestellten Sprache  
- ⏰ funktioniert nur in einem konfigurierbaren Zeitfenster 
- 🔔 kann vor der Ansage einen benutzerdefinierten Ton abspielen
- 🔕 kann die Sprachausgabe deaktivieren (nur Glocke)
- 🏰 kann um 12 Uhr die Westminster-Melodie abspielen

Das Ergebnis ist ein eleganter und dezenter Effekt, ideal für Zuhause oder Büro.

## ✨ Hauptfunktionen

### 🕑 Automatische Zeitansage
- jede Stunde (xx:00)
- jede halbe Stunde (xx:30) – optional

### 🌐 Automatische Mehrsprachenunterstützung
- Italienisch 🇮🇹
- Englisch 🇬🇧
- Französisch 🇫🇷
- Deutsch 🇩🇪 (mit korrekter Behandlung von „halb“)
- Spanisch 🇪🇸

automatischer Fallback auf Italienisch

### ⏱️ Konfigurierbares Zeitfenster
- z. B. nur von 8:00 bis 22:00

###  🔔 Optionale Glocke
- 🎵 12 vordefinierte Sounds zur Auswahl
- 🎶 Möglichkeit zur Verwendung einer eigenen Audiodatei
- 🔕 Alexa-Benachrichtigungssound „announce“ (Standard)

### 🧪 Testfunktion
- zum sofortigen Testen der Ansage

### 🎯 Verhalten

**Glocke (Chime):**
- **Verfügbare Presets**: 12 Sounds wie church-bell, simple-bell, clock-chime usw.
- **Benutzerdefinierter Sound**: „custom“ auswählen und den Pfad zur Audiodatei eingeben
- **Standard**: Alexa-„announce“-Sound (wenn nichts ausgewählt ist)
- **Deaktiviert**: „use_chime“ deaktivieren, um keinen Ton vor der Ansage abzuspielen

**Westminster-Melodie (Tower Clock):**
- Separate Option „tower_clock“
- Spielt **nur um 12:00 Uhr** (Mittag)
- Ersetzt zu dieser Zeit die normale Glocke

**Sprachansage:**
- **Aktiviert** (Standard): Alexa spricht die Uhrzeit nach der Glocke
- **Deaktiviert**: Nur Glocke, keine Sprachansage

**Halbstunden-Ansagen:**
- **Aktiviert** (Standard): Ansagen um :00 und :30
- **Deaktiviert**: Nur Ansagen um :00

## ⚙️ Funktionsweise

Das Herzstück des Systems ist die Klasse:

class DigitalPendulum

die:
- sich bei einem synchronisierten internen Timer registriert (jede Minute bei Sekunde :00)
- überprüft:
  - ob die Integration aktiviert ist
  - ob die Uhrzeit im erlaubten Zeitfenster liegt
  - ob die Minute :00 ist (oder :30, wenn aktiviert)
- den gesprochenen Text anhand der Sprache erstellt
- die Glocke abspielt (falls aktiviert)
- die Sprachansage an das Alexa-Gerät sendet (falls aktiviert)

## 🗣️ Sprachverwaltung

Die Sprache wird automatisch erkannt über:

self.hass.config.language

Beispiele für Ansagen:

| Sprache | Uhrzeit | Ansage |
|------|------|--------|
| 🇮🇹 IT | 10:30 | Ore 10 e trenta |
| 🇬🇧 EN | 14:00 | It's 14 o'clock |
| 🇫🇷 FR | 9:30 | Il est 9 heures trente |
| 🇩🇪 DE | 16:30 | Es ist halb 17 |
| 🇪🇸 ES | 11:00 | Son las 11 |

## 🔔 Glocke (Startsignal)

Wenn die Option use_chime aktiviert ist:
- wird der Alexa-Benachrichtigungston oder der gewählte Sound abgespielt
- das System wartet 1,2 Sekunden
- die Sprachansage startet (falls aktiviert)

Dies erzeugt einen Effekt ähnlich einer echten Pendeluhr 🎶.

## 🧩 Konfigurationsoptionen

| Option | Beschreibung |
|------|------------|
| player | Ziel-Alexa-Gerät |
| start_hour | Startzeit |
| end_hour | Endzeit |
| enabled | Pendel aktivieren/deaktivieren |
| announce_half_hours | Halbstunden-Ansagen aktivieren (sonst nur stündlich) |
| voice_announcement | Sprachansage aktivieren/deaktivieren |
| tower_clock | Westminster-Melodie um 12:00 aktivieren |
| use_chime | Glocke vor der Ansage aktivieren/deaktivieren |
| preset_chime | Auswahl des Glockensounds (12 Presets verfügbar) |
| custom_chime_path | Pfad für benutzerdefinierten Glockensound |

Standardwerte:

- ⏰ start_hour → 8
- ⏰ end_hour → 22
- 🔔 use_chime → True
- 🗣️ voice_announcement → True
- ⏰ announce_half_hours → True
- 🏰 tower_clock → False
- ✅ enabled → True

## 🧪 Soforttest

Eine manuelle Testmethode ist verfügbar:

async_test_announcement()

Die:
- die aktuelle Uhrzeit liest
- einen vollständigen Satz generiert (z. B. „Ore 15 e 42“)
- ihn sofort auf dem Alexa-Gerät abspielt  

Nützlich zur Überprüfung von: Sprache, Lautstärke, Glocke, korrekter TTS-Funktion

## 📦 Anforderungen

> ✨ **Verfügbar über HACS** – vereinfachte Installation und Updates!

- 🏠 Home Assistant 2024.1.0 oder höher
- 🔊 Alexa Media Player installiert und funktionsfähig
- 📡 Alexa-Gerät als Player konfiguriert


## 🎯 Ideale Nutzung

- ✔️ Smarte Häuser
- ✔️ Büros
- ✔️ Gemeinschaftsbereiche
- ✔️ „Modernes Pendel“-Effekt
- ✔️ Unaufdringliche Zeit-Erinnerung

## 🚀 Mögliche zukünftige Erweiterungen

- ⏳ Ansagen alle 15 Minuten
- 🔇 Automatische Nachtlautstärke
- 🗓️ Tagesansage
- 📣 Unterstützung weiterer TTS-Systeme

---
## 

## ☕ Unterstütze das Projekt

Gefällt dir dieses Projekt? Wenn du es nützlich findest, spendiere mir einen virtuellen Kaffee, um zukünftige Entwicklungen zu unterstützen! Jeder noch so kleine Beitrag wird sehr geschätzt. 🙏

**Digital Pendulum ist und bleibt immer kostenlos und Open Source.** Spenden sind vollkommen freiwillig! ❤️


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/dregi56)

💡 **Bevorzugst du andere Methoden?** Du kannst verwenden:

[![revolut](https://img.shields.io/badge/Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/egidio5t9d)
