# 🕰️ Digital Pendulum

A talking digital pendulum for Home Assistant
<br>**Author:** Egidio Ziggiotto (Dregi56)  e-mail: [dregi@cyberservices.com](mailto:dregi@cyberservices.com)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/Dregi56/digital_pendulum)](https://github.com/Dregi56/digital_pendulum/releases)
![License](https://img.shields.io/github/license/Dregi56/digital_pendulum)
[![GitHub stars](https://img.shields.io/github/stars/Dregi56/digital_pendulum?style=social)](https://github.com/Dregi56/digital_pendulum)

🌍 Available languages:
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) |
[Čeština](README.cs.md)

<br>👉 This is the English README. Use the language selector above


## ❤️ Do you like Digital Pendulum?

If you find it useful, consider leaving a ⭐ on GitHub:  
👉 **https://github.com/Dregi56/digital_pendulum**
<br>Thank you.

## 📌 Description

Digital Pendulum is a custom integration for Home Assistant that vocally announces the time, just like a digital pendulum 🕰️.

The system:

- 📢 announces the time every 60, 30, or 15 minutes (configurable interval)
- 🌍 automatically speaks in the language set in Home Assistant
- ⏰ only works within a configurable time slot
- 🔔 can play a custom sound before the announcement
- 🔕 can disable the voice announcement (bell only)
- 🏰 can play the Westminster chime at 12 o'clock
- 🗓️ can announce the day of the week at a chosen hour
- ⏸️ pauses media playback during the announcement, then resumes it
- 📣 supports multiple player devices at once
- 🔊 supports Amazon Alexa, Google Home, other media players and Browser Mod

The result is an elegant and discreet effect, ideal for home or office.

## ✨ Main features

### 🕑 Automatic time announcement
- every hour (xx:00)
- every 30 min (xx:00, xx:30) — optional
- every 15 min (xx:00, xx:15, xx:30, xx:45) — optional

### 🌐 Automatic multilingual support
- Italian 🇮🇹
- English 🇬🇧
- French 🇫🇷
- German 🇩🇪 (with correct handling of "halb" and "Viertel")
- Spanish 🇪🇸
- Czech 🇨🇿 (with grammatically correct forms including quarter-hours)

automatic fallback to English

### ⏱️ Configurable time slot
- e.g. only from 8:00 to 22:00

### 🔔 Optional bell
- 🎵 14 preset sounds to choose from
- 🎶 option to use a custom audio file
- 🔕 Alexa "announce" notification sound (default)

### 🗓️ Day-of-week announcement
- Adds the current day name to the announcement at a configurable hour

### ⏸️ Smart media pause/resume
- If a player is active, it is paused before the announcement and automatically resumed afterwards

### 📣 Multiple player devices
- Select several media_player entities; the announcement is sent to all simultaneously

### 🧪 Test function
- to immediately try the announcement

### 🎯 Behaviour

**Bell (Chime):**
- **Available presets**: 14 sounds including church-bell, simple-bell, clock-chime, etc.
- **Custom sound**: Select "custom" and enter the path of your audio file
- **Default**: Alexa "announce" sound (if you select nothing)
- **Disabled**: Disable "use_chime" for no sound before the announcement

**Westminster Melody (Tower Clock):**
- Separate "tower_clock" option
- Plays **only at 12:00** (noon)
- Replaces the normal chime at that time

**Voice announcement:**
- **Enabled** (default): Player pronounces the time after the bell
- **Disabled**: Bell sound only, no voice announcement

**Announce interval:**
- **60 min** (default): Announcements at :00 only
- **30 min**: Announcements at :00 and :30
- **15 min**: Announcements at :00, :15, :30, and :45

## ⚙️ How it works

Digital Pendulum synchronises with the system clock and automatically checks every minute whether it is time to make an announcement.

**When the announcement triggers:**
1. ⏸️ Pauses any active media playback (if pause_for_announcement is enabled)
2. 🔔 Plays the chosen bell (if enabled)
3. ⏱️ Waits the configured chime delay
4. 🗣️ Player pronounces the time in the Home Assistant language (if enabled)
5. ▶️ Resumes paused playback

Everything happens automatically without the need to configure automations!

## 🗣️ Language handling

The language is automatically detected from `self.hass.config.language`

Announcement examples:

| Language | Time  | Announcement |
|----------|-------|--------------|
| 🇨🇿 CS | 14:00 | Je čtrnáct hodin |
| 🇨🇿 CS | 10:15 | Je čtvrt na jedenáct |
| 🇨🇿 CS | 10:30 | Je půl jedenácté |
| 🇨🇿 CS | 10:45 | Je tři čtvrtě na jedenáct |
| 🇬🇧 EN | 14:00 | It's 14 o'clock |
| 🇬🇧 EN | 10:15 | It's 10 fifteen |
| 🇬🇧 EN | 10:45 | It's 10 forty-five |
| 🇫🇷 FR | 9:30  | Il est 9 heures trente |
| 🇫🇷 FR | 9:15  | Il est 9 heures et quart |
| 🇩🇪 DE | 16:30 | Es ist halb 17 |
| 🇩🇪 DE | 16:15 | Es ist Viertel nach 16 |
| 🇩🇪 DE | 16:45 | Es ist Viertel vor 17 |
| 🇪🇸 ES | 11:00 | Son las 11 |
| 🇮🇹 IT | 10:30 | Ore 10 e trenta |

## 🔔 Chime (initial bell)

If the use_chime option is active:
- the chosen sound is played
- the system waits the configured chime delay
- the voice announcement starts (if enabled)

This creates an effect similar to a real pendulum 🎶.

## 🧩 Configuration options

| Option | Default | Description |
|--------|---------|-------------|
| `player_type` | alexa | Player type (Alexa / Media Player / Browser Mod) |
| `player_device` | — | Target device(s) — supports multiple selection |
| `tts_entity` | — | TTS entity (for Media Player type) |
| `start_hour` | 8 | Operating start time |
| `end_hour` | 22 | Operating end time |
| `enabled` | true | Enables/disables the pendulum |
| `announce_interval` | 60 | Interval in minutes: 60, 30, or 15 |
| `voice_announcement` | true | Enables/disables the voice time announcement |
| `tower_clock` | false | Enables Westminster melody at 12:00 |
| `use_chime` | true | Enables/disables the bell before the announcement |
| `preset_chime` | church-bell | Choice of bell sound (14 available presets) |
| `custom_chime_path` | — | Path for custom bell sound |
| `chime_delay` | 3 s | Wait time between chime and voice announcement |
| `volume` | 15 % | Announcement volume (0 = keep device volume) |
| `announce_day_of_week` | false | Announces the current day name at the chosen hour |
| `day_announce_hour` | 8 | Hour at which the day of week is announced |
| `pause_for_announcement` | true | Pauses media playback during announcement, then resumes |

## 🔊 Setup for Google Home / other media players

1. Select `Media Player` as **Player Type**
2. Select your `media_player.*` entity as **Player Device(s)**
3. Enter your TTS provider as **TTS Entity**, e.g. `tts.google_translate_en_com`
4. Chime sounds are played via `media_player.play_media`

## 🌐 Setup for Browser Mod

1. Install the [Browser Mod](https://github.com/thomasloven/hass-browser_mod) integration
2. Select `Browser Mod` as **Player Type**
3. Select your `media_player.browser_*` entity as **Player Device(s)**
4. Text announcements are shown as browser notifications via `browser_mod.notification`

## 🧪 Immediate test

A manual test method is available:

- Reads the current time
- Generates a complete sentence (e.g. "It's 15 hours and 42 minutes")
- Plays it immediately on the selected device

Useful to verify: language, volume, chime, correct TTS operation

## 📦 Requirements

> ✨ **Available on HACS** - simplified installation and updates!

- 🏠 Home Assistant 2024.1.0 or higher
- 🔊 One of the supported players:
  - Alexa Media Player (for Alexa)
  - Any `media_player` entity (for Google Home, Sonos, etc.)
  - Browser Mod (for browser notifications)

## 💾 Installation

### Via HACS (recommended)

1. Open **HACS** in the side menu
2. Go to **Integrations**
3. Search for **"Digital Pendulum"**
4. Click **Download**
5. **Restart Home Assistant**
6. Go to **Settings** → **Devices & Services** → **Add Integration**
7. Search for **"Digital Pendulum"**
8. Follow the guided configuration

### Manual installation

1. Download the latest release from [GitHub](https://github.com/Dregi56/digital_pendulum/releases)
2. Extract the files
3. Copy the `digital_pendulum` folder to `config/custom_components/`
4. Restart Home Assistant
5. Go to **Settings** → **Devices & Services** → **Add Integration**
6. Search for **"Digital Pendulum"**
7. Follow the guided configuration


## 🎯 Ideal use

- ✔️ Smart homes
- ✔️ Offices
- ✔️ Common areas
- ✔️ "Modern pendulum" effect
- ✔️ Non-invasive time reminder

## 🔧 Troubleshooting

### "Cannot find EU skill" error or Alexa issues

**Alexa Media Player** problem, not Digital Pendulum.

**Quick fix:**
1. Settings → Devices and services → Alexa Media Player
2. Three dots → Reload
3. If it doesn't work: uninstall and reinstall Alexa Media Player

---

### Wrong language

Digital Pendulum automatically uses the Home Assistant language.

1. Check: Settings → System → General → Language
2. Supported languages: 🇮🇹 🇬🇧 🇫🇷 🇩🇪 🇪🇸 🇨🇿
3. After changing the language, restart Home Assistant

---

### No announcements

**Check:**
- Integration enabled? (Switch ON)
- Are you within the configured time slot? (default 8:00-22:00)
- Device online?
- Try the "Test" button

---

### Bell only or voice only

- **Bell only:** Enable "Voice announcement"
- **Voice only:** Enable "Use chime"

---

### Westminster doesn't play at 12

- Check that "Tower Clock" is active
- Works **only at 12:00** (noon, not midnight)

---

### Google Home / Media Player — no voice

- Check that a **TTS Entity** is set (e.g. `tts.google_translate_en_com`)
- Verify the TTS entity exists in Home Assistant (Settings → Devices & Services)

---

### Media resumes too early or too late after announcement

- The pause/resume timing is estimated from the text length
- If it resumes too early, increase the **Chime delay** to give more buffer

---

## 🚀 Possible future developments

- 🔇 Automatic night volume reduction

---

## ☕ Support the project

Do you like this project? If you find it useful, buy me a virtual coffee to support future developments! Every small contribution is greatly appreciated. 🙏

**Digital Pendulum is and will always remain free and open source.** Donations are completely voluntary! ❤️


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/dregi56)

💡 **Prefer other methods?** You can use:

[![revolut](https://img.shields.io/badge/Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/egidio5t9d)
