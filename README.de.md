# 🕰️ Digital Pendulum

Ein sprechendes digitales Pendel für Home Assistant
<br>**Autor:** Egidio Ziggiotto (Dregi56)  e-mail: [dregi@cyberservices.com](mailto:dregi@cyberservices.com)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/Dregi56/digital_pendulum)](https://github.com/Dregi56/digital_pendulum/releases)
![License](https://img.shields.io/github/license/Dregi56/digital_pendulum)
[![GitHub stars](https://img.shields.io/github/stars/Dregi56/digital_pendulum?style=social)](https://github.com/Dregi56/digital_pendulum)

🌍 Verfügbare Sprachen:
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) |
[Čeština](README.cs.md)

<br>👉Dies ist die Deutsche README. Verwenden Sie den Sprachauswähler oben


## ❤️ Gefällt Ihnen Digital Pendulum?

Wenn Sie es nützlich finden, hinterlassen Sie bitte ein ⭐ auf GitHub:  
👉 **https://github.com/Dregi56/digital_pendulum**
<br>Danke.

## 📌 Beschreibung

Digital Pendulum ist eine benutzerdefinierte Integration für Home Assistant, die die Uhrzeit akustisch ansagt, genau wie ein digitales Pendel 🕰️.

Das System:

- 📢 sagt die Uhrzeit alle 60, 30 oder 15 Minuten an (konfigurierbares Intervall)
- 🌍 spricht automatisch in der in Home Assistant eingestellten Sprache
- ⏰ funktioniert nur innerhalb eines konfigurierbaren Zeitfensters
- 🔔 kann vor der Ansage einen benutzerdefinierten Ton abspielen
- 🔕 kann die Sprachansage deaktivieren (nur Glocke)
- 🏰 kann um 12 Uhr die Westminster-Melodie abspielen
- 🗓️ kann den Wochentag zu einer konfigurierbaren Stunde ansagen
- ⏸️ pausiert laufende Wiedergabe vor der Ansage und setzt sie danach fort
- 📣 unterstützt mehrere Abspielgeräte gleichzeitig
- 🔊 unterstützt Amazon Alexa, Google Home, andere Media Player und Browser Mod

Das Ergebnis ist ein eleganter und dezenter Effekt, ideal für Zuhause oder Büro.

## ✨ Hauptfunktionen

### 🕑 Automatische Zeitansage
- jede Stunde (xx:00)
- alle 30 Minuten (xx:00, xx:30) — optional
- alle 15 Minuten (xx:00, xx:15, xx:30, xx:45) — optional

### 🌐 Automatische Mehrsprachunterstützung
- Italienisch 🇮🇹
- Englisch 🇬🇧
- Französisch 🇫🇷
- Deutsch 🇩🇪 (mit korrekter Behandlung von „halb" und „Viertel")
- Spanisch 🇪🇸
- Tschechisch 🇨🇿 (mit grammatikalisch korrekten Formen einschließlich Viertelstunden)

automatischer Fallback auf Englisch

### ⏱️ Konfigurierbares Zeitfenster
- z.B. nur von 8:00 bis 22:00 Uhr

### 🔔 Optionale Glocke
- 🎵 14 voreingestellte Töne zur Auswahl
- 🎶 Möglichkeit, eine benutzerdefinierte Audiodatei zu verwenden
- 🔕 Alexa "announce" Benachrichtigungston (Standard)

### 🗓️ Wochentagsansage
- Fügt den aktuellen Wochentagsnamen zur Ansage einer konfigurierbaren Stunde hinzu

### ⏸️ Intelligente Wiedergabepause
- Falls der Player abspielt, wird er vor der Ansage pausiert und danach automatisch fortgesetzt

### 📣 Mehrere Abspielgeräte
- Wählen Sie mehrere `media_player`-Entitäten; die Ansage wird gleichzeitig an alle gesendet

### 🧪 Testfunktion
- um die Ansage sofort auszuprobieren

### 🎯 Verhalten

**Glocke (Chime):**
- **Verfügbare Presets**: 14 Töne darunter church-bell, clock-chime, usw.
- **Benutzerdefinierter Ton**: Wählen Sie "custom" und geben Sie den Pfad Ihrer Audiodatei ein
- **Standard**: Alexa "announce" Ton (wenn Sie nichts auswählen)
- **Deaktiviert**: Deaktivieren Sie "use_chime" für keinen Ton vor der Ansage

**Westminster-Melodie (Tower Clock):**
- Separate Option "tower_clock"
- Spielt **nur um 12:00 Uhr** (Mittag)
- Ersetzt den normalen Chime zu dieser Zeit

**Sprachansage:**
- **Aktiviert** (Standard): Player spricht die Uhrzeit nach der Glocke aus
- **Deaktiviert**: Nur Glockenton, keine Sprachansage

**Ansageintervall:**
- **60 min** (Standard): Nur zur vollen Stunde
- **30 min**: Um :00 und :30
- **15 min**: Um :00, :15, :30 und :45

## ⚙️ Wie es funktioniert

Digital Pendulum synchronisiert sich mit der Systemuhr und prüft automatisch jede Minute, ob es Zeit für eine Ansage ist.

**Wenn die Ansage ausgelöst wird:**
1. ⏸️ Pausiert laufende Wiedergabe (wenn aktiviert)
2. 🔔 Spielt die gewählte Glocke ab (wenn aktiviert)
3. ⏱️ Wartet die konfigurierte Verzögerung
4. 🗣️ Player spricht die Uhrzeit in der Home Assistant Sprache (wenn aktiviert)
5. ▶️ Setzt die pausierte Wiedergabe fort

Alles geschieht automatisch, ohne Automationen konfigurieren zu müssen!

## 🗣️ Sprachverwaltung

Die Sprache wird automatisch erkannt von `self.hass.config.language`

Ansage-Beispiele:

| Uhrzeit | Ansage |
|---------|--------|
| 14:00 | Es ist 14 Uhr |
| 16:15 | Es ist Viertel nach 16 |
| 16:30 | Es ist halb 17 |
| 16:45 | Es ist Viertel vor 17 |

## 🔔 Chime (Eröffnungsglocke)

Wenn die Option use_chime aktiv ist:
- wird der gewählte Ton abgespielt
- wartet das System die konfigurierte Verzögerung
- beginnt die Sprachansage (wenn aktiviert)

Dies erzeugt einen Effekt ähnlich einem echten Pendel 🎶.

## 🧩 Konfigurationsoptionen

| Option | Standard | Beschreibung |
|--------|----------|--------------|
| `player_type` | alexa | Player-Typ (Alexa / Media Player / Browser Mod) |
| `player_device` | — | Zielgerät(e) — unterstützt Mehrfachauswahl |
| `tts_entity` | — | TTS-Entität (nur für Typ Media Player) |
| `start_hour` | 8 | Betriebsstartzeit |
| `end_hour` | 22 | Betriebsendzeit |
| `enabled` | true | Aktiviert/deaktiviert das Pendel |
| `announce_interval` | 60 | Intervall in Minuten: 60, 30 oder 15 |
| `voice_announcement` | true | Aktiviert/deaktiviert die Sprachzeitansage |
| `tower_clock` | false | Aktiviert Westminster-Melodie um 12:00 Uhr |
| `use_chime` | true | Aktiviert/deaktiviert die Glocke vor der Ansage |
| `preset_chime` | church-bell | Wahl des Glockenklangs (14 verfügbare Presets) |
| `custom_chime_path` | — | Pfad für benutzerdefinierten Glockenklang |
| `chime_delay` | 3 s | Wartezeit zwischen Glocke und Sprachansage |
| `volume` | 15 % | Ansagelautstärke (0 = Gerätelautstärke beibehalten) |
| `announce_day_of_week` | false | Sagt den aktuellen Wochentag zur gewählten Stunde an |
| `day_announce_hour` | 8 | Stunde, zu der der Wochentag angesagt wird |
| `pause_for_announcement` | true | Pausiert Wiedergabe vor der Ansage und setzt sie danach fort |

## 🔧 Fehlerbehebung

### Fehler "Cannot find EU skill" oder Alexa-Probleme

Problem mit **Alexa Media Player**, nicht mit Digital Pendulum.

**Schnelle Lösung:**
1. Einstellungen → Geräte und Dienste → Alexa Media Player
2. Drei Punkte → Neu laden
3. Falls es nicht funktioniert: Alexa Media Player deinstallieren und neu installieren

---

### Falsche Sprache

1. Überprüfen Sie: Einstellungen → System → Allgemein → Sprache
2. Unterstützte Sprachen: 🇮🇹 🇬🇧 🇫🇷 🇩🇪 🇪🇸 🇨🇿
3. Nach dem Ändern der Sprache Home Assistant neu starten

---

### Keine Ansagen

**Überprüfen Sie:**
- Integration aktiviert? (Schalter EIN)
- Im konfigurierten Zeitfenster? (Standard 8:00-22:00 Uhr)
- Gerät online?
- Schaltfläche "Test" versuchen

---

### Westminster läutet nicht um 12 Uhr

- Überprüfen Sie, ob "Tower Clock" aktiv ist
- Funktioniert **nur um 12:00 Uhr** (Mittag, nicht Mitternacht)

---

### Wiedergabe setzt zu früh oder zu spät fort

- Die Pausenzeit wird anhand der Textlänge geschätzt
- Falls zu früh fortgesetzt, erhöhen Sie die **Chime-Verzögerung**

---

## 🚀 Mögliche zukünftige Entwicklungen

- 🔇 Automatische Nachtlautstärke

---

## ☕ Unterstützen Sie das Projekt

Gefällt Ihnen dieses Projekt? Wenn Sie es nützlich finden, spendieren Sie mir einen virtuellen Kaffee, um zukünftige Entwicklungen zu unterstützen! Jeder kleine Beitrag wird sehr geschätzt. 🙏

**Digital Pendulum ist und bleibt immer kostenlos und Open Source.** Spenden sind vollkommen freiwillig! ❤️


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/dregi56)

💡 **Bevorzugen Sie andere Methoden?** Sie können verwenden:

[![revolut](https://img.shields.io/badge/Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/egidio5t9d)
