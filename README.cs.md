# 🕰️ Digital Pendulum

Mluvící digitální kyvadlové hodiny pro Home Assistant
<br>**Autor:** Egidio Ziggiotto (Dregi56)  e-mail: [dregi@cyberservices.com](mailto:dregi@cyberservices.com)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/Dregi56/digital_pendulum)](https://github.com/Dregi56/digital_pendulum/releases)
![License](https://img.shields.io/github/license/Dregi56/digital_pendulum)
[![GitHub stars](https://img.shields.io/github/stars/Dregi56/digital_pendulum?style=social)](https://github.com/Dregi56/digital_pendulum)

🌍 Dostupné jazyky:
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) |
[Čeština](README.cs.md)

<br>👉 Toto je český README. Pro jiný jazyk použijte výběr výše.


## ❤️ Líbí se vám Digital Pendulum?

Pokud vám integration přijde užitečná, zanechte ⭐ na GitHubu:
👉 **https://github.com/Dregi56/digital_pendulum**
<br>Děkuji.

## 📌 Popis

Digital Pendulum je vlastní integrace pro Home Assistant, která hlasově oznamuje čas — stejně jako digitální kyvadlové hodiny 🕰️.

Systém:

- 📢 oznamuje čas každou hodinu a/nebo každou půlhodinu (konfigurovatelné)
- 🌍 automaticky mluví v jazyce nastaveném v Home Assistant
- ⏰ funguje pouze v konfigurovatelném časovém rozsahu
- 🔔 může přehrát vlastní zvuk před oznámením
- 🔕 může zakázat hlasové oznámení (jen zvon)
- 🏰 může přehrát melodii Westminster ve 12 hodin
- 🔊 podporuje Amazon Alexa, Google Home, jiné media přehrávače i Browser Mod

Výsledkem je elegantní a nenápadný efekt, ideální pro domácnost nebo kancelář.

## ✨ Hlavní funkce

### 🕑 Automatické hlášení času
- každou hodinu (xx:00)
- každou půlhodinu (xx:30) – volitelně

### 🌐 Automatická vícejazyčná podpora
- Italština 🇮🇹
- Angličtina 🇬🇧
- Francouzština 🇫🇷
- Němčina 🇩🇪 (se správným „halb")
- Španělština 🇪🇸
- Čeština 🇨🇿 (se správnými gramatickými tvary)

automatický záložní jazyk: italština

### ⏱️ Konfigurovatelný časový rozsah
- např. pouze od 8:00 do 22:00

### 🔔 Volitelný zvon
- 🎵 12 přednastavených zvuků na výběr
- 🎶 možnost použít vlastní audio soubor
- 🔕 výchozí zvuk oznámení (pro Alexa)

### 🔊 Typy přehrávačů
- **Amazon Alexa** – původní chování, `notify.alexa_media`
- **Media Player** – Google Home, Sonos a další; zvuk přes `media_player.play_media`, hlas přes `tts.speak`
- **Browser Mod** – textové oznámení v prohlížeči přes `browser_mod.notification`, zvuk přes `media_player.play_media`

### 🧪 Funkce testu
- okamžitě vyzkoušejte hlášení

### 🎯 Chování

**Zvon (Chime):**
- **Dostupné předvolby**: 12 zvuků včetně church-bell, clock-chime atd.
- **Vlastní zvuk**: Vyberte „custom" a zadejte cestu k audio souboru
- **Výchozí**: zvuk oznámení Alexa (pokud nevyberete nic)
- **Vypnuto**: deaktivujte „use_chime" pro žádný zvuk před oznámením

**Melodie Westminster (Tower Clock):**
- Samostatná možnost „tower_clock"
- Hraje **pouze ve 12:00** (poledne)
- Nahrazuje normální zvon v tuto dobu

**Hlasové oznámení:**
- **Zapnuto** (výchozí): přehrávač vysloví čas po zvonu
- **Vypnuto**: pouze zvon, žádné hlasové oznámení

**Oznámení půlhodiny:**
- **Zapnuto** (výchozí): oznámení v :00 a :30
- **Vypnuto**: pouze oznámení v :00

## ⚙️ Jak to funguje

Digital Pendulum se synchronizuje se systémovými hodinami a automaticky každou minutu kontroluje, zda je čas na oznámení.

**Když se oznámení spustí:**
1. 🔔 Přehraje zvolený zvon (pokud je zapnut)
2. ⏱️ Čeká 1,2 sekundy
3. 🗣️ Přehrávač vysloví čas v jazyce Home Assistant (pokud je zapnuto)

Vše probíhá automaticky bez nutnosti konfigurovat automatizace!

## 🗣️ Zpracování jazyka

Jazyk je automaticky detekován z:

```
self.hass.config.language
```

Příklady oznámení:

| Jazyk | Čas | Oznámení |
|-------|-----|----------|
| 🇨🇿 CS | 10:30 | Je půl jedenácté |
| 🇨🇿 CS | 14:00 | Je čtrnáct hodin |
| 🇨🇿 CS | 1:00 | Je jedna hodina |
| 🇨🇿 CS | 2:00 | Jsou dvě hodiny |
| 🇬🇧 EN | 14:00 | It's 14 o'clock |
| 🇩🇪 DE | 16:30 | Es ist halb 17 |

## 🔔 Zvon (počáteční zvonění)

Pokud je aktivní možnost use_chime:
- přehraje se zvolený zvuk
- systém čeká 1,2 sekundy
- spustí se hlasové oznámení (pokud je zapnuto)

Tím vzniká efekt podobný skutečným kyvadlovým hodinám 🎶.

## 🧩 Možnosti konfigurace

| Možnost | Popis |
|---------|-------|
| player_type | Typ přehrávače (Alexa / Media Player / Browser Mod) |
| player_device | Cílové zařízení (media_player entita) |
| tts_entity | Entita TTS (jen pro typ Media Player, např. `tts.google_translate_cs`) |
| start_hour | Čas začátku provozu |
| end_hour | Čas konce provozu |
| enabled | Zapíná/vypíná kyvadlové hodiny |
| announce_half_hours | Zapíná oznámení každou půlhodinu (jinak každou hodinu) |
| voice_announcement | Zapíná/vypíná hlasové oznámení času |
| tower_clock | Zapíná melodii Westminster ve 12:00 |
| use_chime | Zapíná/vypíná zvon před oznámením |
| preset_chime | Výběr zvuku zvonu (12 dostupných předvoleb) |
| custom_chime_path | Cesta k vlastnímu zvuku zvonu |

Výchozí hodnoty:

- ⏰ start_hour → 8
- ⏰ end_hour → 22
- 🔔 use_chime → True
- 🗣️ voice_announcement → True
- ⏰ announce_half_hours → True
- 🏰 tower_clock → False
- ✅ enabled → True

## 🔊 Nastavení pro Google Home / jiné media přehrávače

1. Jako **Typ přehrávače** vyberte `Media Player`
2. Jako **Zařízení přehrávače** vyberte svůj `media_player.*` (Google Home, Sonos atd.)
3. Jako **Entitu TTS** zadejte svého poskytovatele TTS, např. `tts.google_translate_cs`
4. Zvuky zvonu se přehrávají přes `media_player.play_media`

## 🌐 Nastavení pro Browser Mod

1. Nainstalujte integraci [Browser Mod](https://github.com/thomasloven/hass-browser_mod)
2. Jako **Typ přehrávače** vyberte `Browser Mod`
3. Jako **Zařízení přehrávače** vyberte `media_player.browser_*` entitu
4. Textová oznámení se zobrazují jako notifikace v prohlížeči (`browser_mod.notification`)
5. Zvuky zvonu se přehrávají přes `media_player.play_media`

## 🧪 Okamžitý test

Je dostupná ruční testovací metoda, která:
- přečte aktuální čas
- vygeneruje kompletní větu (např. „Je čtrnáct hodin a 42 minut")
- okamžitě ji přehraje na vybraném zařízení

Užitečné pro ověření: jazyk, hlasitost, zvon, správná funkce TTS

## 📦 Požadavky

> ✨ **Dostupné na HACS** – zjednodušená instalace a aktualizace!

- 🏠 Home Assistant 2024.1.0 nebo vyšší
- 🔊 Jeden z podporovaných přehrávačů:
  - Alexa Media Player (pro Alexa)
  - Libovolný `media_player` (pro Google Home, Sonos atd.)
  - Browser Mod (pro oznámení v prohlížeči)

## 💾 Instalace

### Přes HACS (doporučeno)

1. Otevřete **HACS** v bočním menu
2. Přejděte na **Integrace**
3. Vyhledejte **„Digital Pendulum"**
4. Klikněte na **Stáhnout**
5. **Restartujte Home Assistant**
6. Přejděte do **Nastavení** → **Zařízení a služby** → **Přidat integraci**
7. Vyhledejte **„Digital Pendulum"**
8. Postupujte podle průvodce konfigurací

### Ruční instalace

1. Stáhněte nejnovější verzi z [GitHubu](https://github.com/Dregi56/digital_pendulum/releases)
2. Rozbalte soubory
3. Zkopírujte složku `digital_pendulum` do `config/custom_components/`
4. Restartujte Home Assistant
5. Přejděte do **Nastavení** → **Zařízení a služby** → **Přidat integraci**
6. Vyhledejte **„Digital Pendulum"**
7. Postupujte podle průvodce konfigurací

## 🎯 Ideální použití

- ✔️ Chytré domácnosti
- ✔️ Kanceláře
- ✔️ Společné prostory
- ✔️ Efekt „moderních kyvadlových hodin"
- ✔️ Nenápadná časová připomínka

## 🔧 Řešení problémů

### Špatný jazyk

Digital Pendulum automaticky používá jazyk Home Assistant.

1. Zkontrolujte: Nastavení → Systém → Obecné → Jazyk → nastavte `Čeština`
2. Podporované jazyky: 🇮🇹 🇬🇧 🇫🇷 🇩🇪 🇪🇸 🇨🇿
3. Po změně jazyka restartujte Home Assistant

---

### Žádná oznámení

**Zkontrolujte:**
- Je integrace zapnuta? (přepínač ON)
- Jste v nastaveném časovém rozsahu? (výchozí 8:00–22:00)
- Je zařízení online?
- Vyzkoušejte tlačítko „Test"

---

### Pouze zvon nebo pouze hlas

- **Pouze zvon:** Zapněte „Hlasové oznámení"
- **Pouze hlas:** Zapněte „Použít zvuk zvonu"

---

### Westminster nehraje ve 12

- Zkontrolujte, zda je aktivní „Tower Clock"
- Funguje **pouze ve 12:00** (poledne, ne půlnoc)

---

### Google Home / Media Player — žádný hlas

- Zkontrolujte, zda je nastavena **Entita TTS** (např. `tts.google_translate_cs`)
- Ověřte, zda TTS entita existuje v Home Assistant (Nastavení → Zařízení a služby)

---

### Browser Mod — žádné oznámení

- Ověřte, zda je Browser Mod správně nainstalován a připojen
- Zkontrolujte, zda jste vybrali správnou `media_player.browser_*` entitu

---

## 🚀 Možný budoucí vývoj

- ⏳ Oznámení každých 15 minut
- 🔇 Automatická noční hlasitost
- 🗓️ Oznámení dne
- 📣 Podpora dalších TTS

---

## ☕ Podpořte projekt

Líbí se vám tento projekt? Pokud vám přijde užitečný, kupte mi virtuální kávu na podporu budoucího vývoje! Každý malý příspěvek je velmi oceňován. 🙏

**Digital Pendulum je a vždy zůstane zdarma a open source.** Dary jsou zcela dobrovolné! ❤️


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/dregi56)

💡 **Preferujete jinou metodu?** Můžete použít:

[![revolut](https://img.shields.io/badge/Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/egidio5t9d)
