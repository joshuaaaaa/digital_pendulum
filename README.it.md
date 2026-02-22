# 🕰️ Digital Pendulum

Un pendolo digitale parlante per Home Assistant
<br>**Autore:** Egidio Ziggiotto (Dregi56)  e-mail: [dregi@cyberservices.com](mailto:dregi@cyberservices.com)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/Dregi56/digital_pendulum)](https://github.com/Dregi56/digital_pendulum/releases)
![License](https://img.shields.io/github/license/Dregi56/digital_pendulum)
[![GitHub stars](https://img.shields.io/github/stars/Dregi56/digital_pendulum?style=social)](https://github.com/Dregi56/digital_pendulum)

🌍 Lingue disponibili:
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) |
[Čeština](README.cs.md)

<br>👉This is the Italian README. Use the language selector above


## ❤️ Ti piace Digital Pendulum?

Se ti è utile, considera di lasciare una ⭐ su GitHub:  
👉 **https://github.com/Dregi56/digital_pendulum**
<br>Grazie.

## 📌 Descrizione

Digital Pendulum è un'integrazione personalizzata per Home Assistant che annuncia vocalmente l'orario, proprio come un pendolo digitale 🕰️.

Il sistema:

- 📢 annuncia l'orario ogni 60, 30 o 15 minuti (intervallo configurabile)
- 🌍 parla automaticamente nella lingua impostata in Home Assistant
- ⏰ funziona solo in una fascia oraria configurabile
- 🔔 può riprodurre un suono personalizzato prima dell'annuncio
- 🔕 può disabilitare l'annuncio vocale (solo campana)
- 🏰 può riprodurre la melodia Westminster alle ore 12
- 🗓️ può annunciare il giorno della settimana a un'ora configurabile
- ⏸️ mette in pausa la riproduzione prima dell'annuncio e la riprende dopo
- 📣 supporta più dispositivi player contemporaneamente
- 🔊 supporta Amazon Alexa, Google Home, altri media player e Browser Mod

Il risultato è un effetto elegante e discreto, ideale per casa o ufficio.

## ✨ Funzionalità principali

### 🕑 Annuncio automatico dell'orario
- ogni ora (xx:00)
- ogni 30 minuti (xx:00, xx:30) — opzionale
- ogni 15 minuti (xx:00, xx:15, xx:30, xx:45) — opzionale

### 🌐 Supporto multilingua automatico
- Italiano 🇮🇹
- Inglese 🇬🇧
- Francese 🇫🇷
- Tedesco 🇩🇪 (con gestione corretta di "halb" e "Viertel")
- Spagnolo 🇪🇸
- Ceco 🇨🇿 (con forme grammaticalmente corrette inclusi i quarti d'ora)

fallback automatico all'inglese

### ⏱️ Fascia oraria configurabile
- es. solo dalle 8:00 alle 22:00

### 🔔 Campana opzionale
- 🎵 14 suoni predefiniti tra cui scegliere
- 🎶 possibilità di usare un file audio personalizzato
- 🔕 suono di notifica "announce" di Alexa (default)

### 🗓️ Annuncio del giorno della settimana
- Aggiunge il nome del giorno corrente all'annuncio a un'ora configurabile (default 8:00)

### ⏸️ Pausa intelligente della riproduzione
- Se il player sta riproducendo, viene messo in pausa prima dell'annuncio e ripreso automaticamente dopo

### 📣 Più dispositivi player
- Seleziona più entità `media_player`; l'annuncio viene inviato a tutte simultaneamente

### 🧪 Funzione di test
- per provare immediatamente l'annuncio

### 🎯 Comportamento

**Campana (Chime):**
- **Preset disponibili**: 14 suoni tra cui church-bell, clock-chime, ecc.
- **Suono personalizzato**: Seleziona "custom" e inserisci il path del tuo file audio
- **Default**: Suono "announce" di Alexa (se non selezioni nulla)
- **Disattivato**: Disabilita "use_chime" per nessun suono prima dell'annuncio

**Melodia Westminster (Tower Clock):**
- Opzione separata "tower_clock"
- Suona **solo alle ore 12:00** (mezzogiorno)
- Sostituisce il chime normale a quell'ora

**Annuncio vocale:**
- **Abilitato** (default): Player pronuncia l'ora dopo la campana
- **Disabilitato**: Solo suono campana, nessun annuncio vocale

**Intervallo annunci:**
- **60 min** (default): Solo alla :00
- **30 min**: Alle :00 e :30
- **15 min**: Alle :00, :15, :30 e :45

## ⚙️ Come funziona

Digital Pendulum si sincronizza con l'orologio di sistema e controlla automaticamente ogni minuto se è il momento di fare un annuncio.

**Quando scatta l'annuncio:**
1. ⏸️ Mette in pausa la riproduzione attiva (se abilitato)
2. 🔔 Riproduce la campana scelta (se abilitata)
3. ⏱️ Attende il ritardo configurato
4. 🗣️ Player pronuncia l'ora nella lingua di Home Assistant (se abilitata)
5. ▶️ Riprende la riproduzione in pausa

Tutto avviene automaticamente senza bisogno di configurare automazioni!

## 🗣️ Gestione delle lingue

La lingua viene rilevata automaticamente da `self.hass.config.language`

Esempi di annunci:

| Orario | Annuncio |
|--------|----------|
| 10:00 | Ore 10 |
| 10:15 | Ore 10 e quindici |
| 10:30 | Ore 10 e trenta |
| 10:45 | Ore 10 e quarantacinque |

## 🧩 Opzioni di configurazione

| Opzione | Default | Descrizione |
|---------|---------|-------------|
| `player_type` | alexa | Tipo player (Alexa / Media Player / Browser Mod) |
| `player_device` | — | Dispositivo/i target — supporta selezione multipla |
| `tts_entity` | — | Entità TTS (solo per tipo Media Player) |
| `start_hour` | 8 | Ora di inizio funzionamento |
| `end_hour` | 22 | Ora di fine funzionamento |
| `enabled` | true | Abilita/disabilita il pendolo |
| `announce_interval` | 60 | Intervallo in minuti: 60, 30 o 15 |
| `voice_announcement` | true | Abilita/disabilita l'annuncio vocale dell'ora |
| `tower_clock` | false | Abilita melodia Westminster alle ore 12:00 |
| `use_chime` | true | Attiva/disattiva la campana prima dell'annuncio |
| `preset_chime` | church-bell | Scelta del suono campana (14 preset disponibili) |
| `custom_chime_path` | — | Path per suono campana personalizzato |
| `chime_delay` | 3 s | Attesa tra campana e annuncio vocale |
| `volume` | 15 % | Volume annuncio (0 = mantieni volume dispositivo) |
| `announce_day_of_week` | false | Annuncia il giorno corrente all'ora scelta |
| `day_announce_hour` | 8 | Ora in cui viene aggiunto il nome del giorno |
| `pause_for_announcement` | true | Mette in pausa la riproduzione durante l'annuncio e la riprende dopo |

## 🔧 Risoluzione problemi

### Errore "Cannot find EU skill" o problemi Alexa

Problema di **Alexa Media Player**, non di Digital Pendulum.

**Soluzione rapida:**
1. Impostazioni → Dispositivi e servizi → Alexa Media Player
2. Tre puntini → Ricarica
3. Se non funziona: disinstalla e reinstalla Alexa Media Player

---

### Lingua sbagliata

1. Verifica: Impostazioni → Sistema → Generali → Lingua
2. Lingue supportate: 🇮🇹 🇬🇧 🇫🇷 🇩🇪 🇪🇸 🇨🇿
3. Dopo aver cambiato lingua, riavvia Home Assistant

---

### Nessun annuncio

**Controlla:**
- Integrazione abilitata? (Interruttore ON)
- Nell'orario configurato? (default 8:00-22:00)
- Dispositivo online?
- Prova il pulsante "Test"

---

### Westminster non suona alle 12

- Verifica che "Tower Clock" sia attivo
- Funziona **solo alle 12:00** (mezzogiorno, non mezzanotte)

---

### La riproduzione riprende troppo presto o tardi

- La durata della pausa è stimata in base alla lunghezza del testo
- Se riprende troppo presto, aumenta il **ritardo del chime**

---

## 🚀 Possibili evoluzioni future

- 🔇 Volume automatico notturno

---

## ☕ Supporta il progetto

Ti piace questo progetto? Se lo trovi utile, offrimi un caffè virtuale per sostenere le evoluzioni future! Ogni piccolo contributo è super apprezzato. 🙏

**Digital Pendulum è e rimarrà sempre gratuito e open source.** Le donazioni sono completamente volontarie! ❤️


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/dregi56)

💡 **Preferisci altri metodi?** Puoi usare:

[![revolut](https://img.shields.io/badge/Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/egidio5t9d)
