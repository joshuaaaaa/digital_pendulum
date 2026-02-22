# 🕰️ Digital Pendulum

Un péndulo digital parlante para Home Assistant
<br>**Autor:** Egidio Ziggiotto (Dregi56)  e-mail: [dregi@cyberservices.com](mailto:dregi@cyberservices.com)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/Dregi56/digital_pendulum)](https://github.com/Dregi56/digital_pendulum/releases)
![License](https://img.shields.io/github/license/Dregi56/digital_pendulum)
[![GitHub stars](https://img.shields.io/github/stars/Dregi56/digital_pendulum?style=social)](https://github.com/Dregi56/digital_pendulum)

🌍 Idiomas disponibles:
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) |
[Čeština](README.cs.md)

<br>👉Este es el README en Español. Usa el selector de idioma arriba


## ❤️ ¿Te gusta Digital Pendulum?

Si te resulta útil, considera dejar una ⭐ en GitHub:  
👉 **https://github.com/Dregi56/digital_pendulum**
<br>Gracias.

## 📌 Descripción

Digital Pendulum es una integración personalizada para Home Assistant que anuncia vocalmente la hora, igual que un péndulo digital 🕰️.

El sistema:

- 📢 anuncia la hora cada 60, 30 o 15 minutos (intervalo configurable)
- 🌍 habla automáticamente en el idioma configurado en Home Assistant
- ⏰ funciona solo en una franja horaria configurable
- 🔔 puede reproducir un sonido personalizado antes del anuncio
- 🔕 puede deshabilitar el anuncio de voz (solo campana)
- 🏰 puede reproducir la melodía Westminster a las 12 horas
- 🗓️ puede anunciar el día de la semana a una hora configurable
- ⏸️ pausa la reproducción durante el anuncio y la reanuda después
- 📣 admite varios dispositivos reproductores a la vez
- 🔊 admite Amazon Alexa, Google Home, otros media players y Browser Mod

El resultado es un efecto elegante y discreto, ideal para el hogar o la oficina.

## ✨ Funcionalidades principales

### 🕑 Anuncio automático de la hora
- cada hora (xx:00)
- cada 30 min (xx:00, xx:30) — opcional
- cada 15 min (xx:00, xx:15, xx:30, xx:45) — opcional

### 🌐 Soporte multilingüe automático
- Italiano 🇮🇹
- Inglés 🇬🇧
- Francés 🇫🇷
- Alemán 🇩🇪 (con gestión correcta de "halb" y "Viertel")
- Español 🇪🇸
- Checo 🇨🇿 (con formas gramaticalmente correctas incluidos los cuartos de hora)

fallback automático al inglés

### ⏱️ Franja horaria configurable
- ej. solo de 8:00 a 22:00

### 🔔 Campana opcional
- 🎵 14 sonidos predefinidos para elegir
- 🎶 posibilidad de usar un archivo de audio personalizado
- 🔕 sonido de notificación "announce" de Alexa (por defecto)

### 🗓️ Anuncio del día de la semana
- Añade el nombre del día actual al anuncio a una hora configurable (por defecto 8:00)

### ⏸️ Pausa inteligente de la reproducción
- Si el reproductor está activo, se pausa antes del anuncio y se reanuda automáticamente después

### 📣 Varios dispositivos reproductores
- Selecciona varias entidades `media_player`; el anuncio se envía a todas simultáneamente

### 🧪 Función de prueba
- para probar el anuncio inmediatamente

### 🎯 Comportamiento

**Campana (Chime):**
- **Presets disponibles**: 14 sonidos entre los que se incluyen church-bell, clock-chime, etc.
- **Sonido personalizado**: Selecciona "custom" e introduce la ruta de tu archivo de audio
- **Por defecto**: Sonido "announce" de Alexa (si no seleccionas nada)
- **Desactivado**: Deshabilita "use_chime" para ningún sonido antes del anuncio

**Melodía Westminster (Tower Clock):**
- Opción separada "tower_clock"
- Suena **solo a las 12:00** (mediodía)
- Sustituye el chime normal a esa hora

**Anuncio de voz:**
- **Habilitado** (por defecto): Reproductor pronuncia la hora después de la campana
- **Deshabilitado**: Solo sonido de campana, ningún anuncio de voz

**Intervalo de anuncio:**
- **60 min** (por defecto): Solo en :00
- **30 min**: En :00 y :30
- **15 min**: En :00, :15, :30 y :45

## ⚙️ Cómo funciona

Digital Pendulum se sincroniza con el reloj del sistema y comprueba automáticamente cada minuto si es el momento de hacer un anuncio.

**Cuando se activa el anuncio:**
1. ⏸️ Pausa la reproducción activa (si está habilitado)
2. 🔔 Reproduce la campana elegida (si está habilitada)
3. ⏱️ Espera el retardo configurado
4. 🗣️ Reproductor pronuncia la hora en el idioma de Home Assistant (si está habilitado)
5. ▶️ Reanuda la reproducción pausada

¡Todo ocurre automáticamente sin necesidad de configurar automatizaciones!

## 🗣️ Gestión de idiomas

El idioma se detecta automáticamente desde `self.hass.config.language`

Ejemplos de anuncios:

| Hora  | Anuncio |
|-------|---------|
| 11:00 | Son las 11 |
| 11:15 | Son las 11 y cuarto |
| 11:30 | Son las 11 y media |
| 11:45 | Son las 11 y cuarenta y cinco |
| 1:00  | Es la una |
| 1:15  | Es la una y cuarto |

## 🧩 Opciones de configuración

| Opción | Por defecto | Descripción |
|--------|-------------|-------------|
| `player_type` | alexa | Tipo de reproductor (Alexa / Media Player / Browser Mod) |
| `player_device` | — | Dispositivo(s) objetivo — admite selección múltiple |
| `tts_entity` | — | Entidad TTS (solo para tipo Media Player) |
| `start_hour` | 8 | Hora de inicio de funcionamiento |
| `end_hour` | 22 | Hora de fin de funcionamiento |
| `enabled` | true | Habilita/deshabilita el péndulo |
| `announce_interval` | 60 | Intervalo en minutos: 60, 30 o 15 |
| `voice_announcement` | true | Habilita/deshabilita el anuncio de voz de la hora |
| `tower_clock` | false | Habilita melodía Westminster a las 12:00 |
| `use_chime` | true | Activa/desactiva la campana antes del anuncio |
| `preset_chime` | church-bell | Elección del sonido de campana (14 presets disponibles) |
| `custom_chime_path` | — | Ruta para sonido de campana personalizado |
| `chime_delay` | 3 s | Espera entre campana y anuncio de voz |
| `volume` | 15 % | Volumen del anuncio (0 = mantener volumen del dispositivo) |
| `announce_day_of_week` | false | Anuncia el día actual a la hora elegida |
| `day_announce_hour` | 8 | Hora a la que se añade el nombre del día |
| `pause_for_announcement` | true | Pausa la reproducción durante el anuncio y la reanuda después |

## 🔧 Resolución de problemas

### Error "Cannot find EU skill" o problemas con Alexa

Problema de **Alexa Media Player**, no de Digital Pendulum.

**Solución rápida:**
1. Ajustes → Dispositivos y servicios → Alexa Media Player
2. Tres puntos → Recargar
3. Si no funciona: desinstala y reinstala Alexa Media Player

---

### Idioma incorrecto

1. Verifica: Ajustes → Sistema → General → Idioma
2. Idiomas soportados: 🇮🇹 🇬🇧 🇫🇷 🇩🇪 🇪🇸 🇨🇿
3. Después de cambiar el idioma, reinicia Home Assistant

---

### Ningún anuncio

**Comprueba:**
- ¿Integración habilitada? (Interruptor ON)
- ¿Dentro de la franja horaria? (por defecto 8:00-22:00)
- ¿Dispositivo en línea?
- Prueba el botón "Test"

---

### Westminster no suena a las 12

- Verifica que "Tower Clock" esté activo
- Funciona **solo a las 12:00** (mediodía, no medianoche)

---

### La reproducción se reanuda demasiado pronto o tarde

- La duración de la pausa se estima a partir de la longitud del texto
- Si reanuda demasiado pronto, aumenta el **retardo del chime**

---

## 🚀 Posibles evoluciones futuras

- 🔇 Volumen automático nocturno

---

## ☕ Apoya el proyecto

¿Te gusta este proyecto? Si te resulta útil, ¡invítame a un café virtual para apoyar los desarrollos futuros! Cada pequeña contribución es muy apreciada. 🙏

**Digital Pendulum es y seguirá siendo siempre gratuito y de código abierto.** ¡Las donaciones son completamente voluntarias! ❤️


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/dregi56)

💡 **¿Prefieres otros métodos?** Puedes usar:

[![revolut](https://img.shields.io/badge/Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/egidio5t9d)
