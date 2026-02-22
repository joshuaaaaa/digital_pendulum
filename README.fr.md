# 🕰️ Digital Pendulum

Un pendule numérique parlant pour Home Assistant
<br>**Auteur:** Egidio Ziggiotto (Dregi56)  e-mail: [dregi@cyberservices.com](mailto:dregi@cyberservices.com)



🌍 Langues disponibles:
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) |
[Čeština](README.cs.md)

<br>👉Ceci est le README en Français. Utilisez le sélecteur de langue ci-dessus

## http://buymeacoffee.com/jakubhruby

<img width="150" height="150" alt="qr-code" src="https://github.com/user-attachments/assets/2581bf36-7f7d-4745-b792-d1abaca6e57d" />

## 📌 Description

Digital Pendulum est une intégration personnalisée pour Home Assistant qui annonce vocalement l'heure, tout comme une pendule numérique 🕰️.

Le système :

- 📢 annonce l'heure toutes les 60, 30 ou 15 minutes (intervalle configurable)
- 🌍 parle automatiquement dans la langue configurée dans Home Assistant
- ⏰ fonctionne uniquement dans une plage horaire configurable
- 🔔 peut reproduire un son personnalisé avant l'annonce
- 🔕 peut désactiver l'annonce vocale (sonnerie uniquement)
- 🏰 peut reproduire la mélodie Westminster à 12 heures
- 🗓️ peut annoncer le jour de la semaine à une heure configurable
- ⏸️ met en pause la lecture pendant l'annonce et la reprend ensuite
- 📣 prend en charge plusieurs appareils lecteurs simultanément
- 🔊 prend en charge Amazon Alexa, Google Home, d'autres media players et Browser Mod

Le résultat est un effet élégant et discret, idéal pour la maison ou le bureau.

## ✨ Fonctionnalités principales

### 🕑 Annonce automatique de l'heure
- toutes les heures (xx:00)
- toutes les 30 min (xx:00, xx:30) — optionnel
- toutes les 15 min (xx:00, xx:15, xx:30, xx:45) — optionnel

### 🌐 Support multilingue automatique
- Italien 🇮🇹
- Anglais 🇬🇧
- Français 🇫🇷
- Allemand 🇩🇪 (avec gestion correcte de "halb" et "Viertel")
- Espagnol 🇪🇸
- Tchèque 🇨🇿 (avec formes grammaticalement correctes incluant les quarts d'heure)

fallback automatique en anglais

### ⏱️ Plage horaire configurable
- ex. uniquement de 8h00 à 22h00

### 🔔 Sonnerie optionnelle
- 🎵 14 sons prédéfinis au choix
- 🎶 possibilité d'utiliser un fichier audio personnalisé
- 🔕 son de notification "announce" d'Alexa (par défaut)

### 🗓️ Annonce du jour de la semaine
- Ajoute le nom du jour en cours à l'annonce à une heure configurable (par défaut 8h00)

### ⏸️ Pause intelligente de la lecture
- Si le lecteur est en cours de lecture, il est mis en pause avant l'annonce et reprend automatiquement ensuite

### 📣 Plusieurs appareils lecteurs
- Sélectionnez plusieurs entités `media_player` ; l'annonce est envoyée à toutes simultanément

### 🧪 Fonction de test
- pour essayer l'annonce immédiatement

### 🎯 Comportement

**Sonnerie (Chime) :**
- **Presets disponibles** : 14 sons dont church-bell, clock-chime, etc.
- **Son personnalisé** : Sélectionnez "custom" et entrez le chemin de votre fichier audio
- **Par défaut** : Son "announce" d'Alexa (si vous ne sélectionnez rien)
- **Désactivé** : Désactivez "use_chime" pour aucun son avant l'annonce

**Mélodie Westminster (Tower Clock) :**
- Option séparée "tower_clock"
- Sonne **uniquement à 12h00** (midi)
- Remplace le chime normal à cette heure

**Annonce vocale :**
- **Activée** (par défaut) : Le lecteur prononce l'heure après la sonnerie
- **Désactivée** : Son de sonnerie uniquement, aucune annonce vocale

**Intervalle d'annonce :**
- **60 min** (par défaut) : Uniquement à la :00
- **30 min** : À :00 et :30
- **15 min** : À :00, :15, :30 et :45

## ⚙️ Comment ça fonctionne

Digital Pendulum se synchronise avec l'horloge système et vérifie automatiquement chaque minute s'il est temps de faire une annonce.

**Quand l'annonce se déclenche :**
1. ⏸️ Met en pause la lecture active (si activé)
2. 🔔 Reproduit la sonnerie choisie (si activée)
3. ⏱️ Attend le délai configuré
4. 🗣️ Le lecteur prononce l'heure dans la langue de Home Assistant (si activée)
5. ▶️ Reprend la lecture en pause

Tout se passe automatiquement sans avoir besoin de configurer des automatisations !

## 🗣️ Gestion des langues

La langue est détectée automatiquement depuis `self.hass.config.language`

Exemples d'annonces :

| Heure | Annonce |
|-------|---------|
| 9:00  | Il est 9 heures |
| 9:15  | Il est 9 heures et quart |
| 9:30  | Il est 9 heures trente |
| 9:45  | Il est 9 heures moins le quart |

## 🧩 Options de configuration

| Option | Par défaut | Description |
|--------|------------|-------------|
| `player_type` | alexa | Type de lecteur (Alexa / Media Player / Browser Mod) |
| `player_device` | — | Appareil(s) cible — prend en charge la sélection multiple |
| `tts_entity` | — | Entité TTS (uniquement pour type Media Player) |
| `start_hour` | 8 | Heure de début de fonctionnement |
| `end_hour` | 22 | Heure de fin de fonctionnement |
| `enabled` | true | Active/désactive la pendule |
| `announce_interval` | 60 | Intervalle en minutes : 60, 30 ou 15 |
| `voice_announcement` | true | Active/désactive l'annonce vocale de l'heure |
| `tower_clock` | false | Active la mélodie Westminster à 12h00 |
| `use_chime` | true | Active/désactive la sonnerie avant l'annonce |
| `preset_chime` | church-bell | Choix du son de sonnerie (14 presets disponibles) |
| `custom_chime_path` | — | Chemin pour son de sonnerie personnalisé |
| `chime_delay` | 3 s | Attente entre sonnerie et annonce vocale |
| `volume` | 15 % | Volume de l'annonce (0 = conserver le volume de l'appareil) |
| `announce_day_of_week` | false | Annonce le jour actuel à l'heure choisie |
| `day_announce_hour` | 8 | Heure à laquelle le nom du jour est ajouté |
| `pause_for_announcement` | true | Met en pause la lecture pendant l'annonce et la reprend ensuite |

## 🔧 Résolution des problèmes

### Erreur "Cannot find EU skill" ou problèmes Alexa

Problème d'**Alexa Media Player**, pas de Digital Pendulum.

**Solution rapide :**
1. Paramètres → Appareils et services → Alexa Media Player
2. Trois points → Recharger
3. Si ça ne fonctionne pas : désinstallez et réinstallez Alexa Media Player

---

### Mauvaise langue

1. Vérifiez : Paramètres → Système → Général → Langue
2. Langues supportées : 🇮🇹 🇬🇧 🇫🇷 🇩🇪 🇪🇸 🇨🇿
3. Après avoir changé la langue, redémarrez Home Assistant

---

### Aucune annonce

**Vérifiez :**
- Intégration activée ? (Interrupteur ON)
- Dans la plage horaire configurée ? (par défaut 8h00-22h00)
- Appareil en ligne ?
- Essayez le bouton "Test"

---

### Westminster ne sonne pas à 12h

- Vérifiez que "Tower Clock" est actif
- Fonctionne **uniquement à 12h00** (midi, pas minuit)

---

### La lecture reprend trop tôt ou trop tard

- La durée de la pause est estimée d'après la longueur du texte
- Si elle reprend trop tôt, augmentez le **délai du chime**

---

## 🚀 Évolutions futures possibles

- 🔇 Volume automatique nocturne

---


