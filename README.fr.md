# 🕰️ Digital Pendulum

Un pendule numérique parlant pour Home Assistant  
<br>**Auteur :** Egidio Ziggiotto (Dregi56)  e-mail : [dregi@cyberservices.com](mailto:dregi@cyberservices.com)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/Dregi56/digital_pendulum)](https://github.com/Dregi56/digital_pendulum/releases)
![License](https://img.shields.io/github/license/Dregi56/digital_pendulum)
[![GitHub stars](https://img.shields.io/github/stars/Dregi56/digital_pendulum?style=social)](https://github.com/Dregi56/digital_pendulum)

🌍 Langues disponibles :
[Italiano](README.it.md) |
[English](README.en.md) |
[Español](README.es.md) |
[Deutsch](README.de.md) |
[Français](README.fr.md) 
<br>👉Ceci est le README en français. Utilisez le sélecteur de langue ci-dessus


## ❤️ Vous aimez Digital Pendulum ?

Si cela vous est utile, pensez à laisser une ⭐ sur GitHub :  
👉 **https://github.com/Dregi56/digital_pendulum**
<br>Merci.

## 📌 Description

Digital Pendulum est une intégration personnalisée pour Home Assistant qui annonce vocalement l’heure, comme un pendule numérique 🕰️.


En utilisant un appareil Alexa comme haut-parleur, le système :

- 📢 annonce l’heure toutes les heures et/ou toutes les demi-heures (configurable)
- 🌍 parle automatiquement dans la langue définie dans Home Assistant  
- ⏰ fonctionne uniquement dans une plage horaire configurable 
- 🔔 peut jouer un son personnalisé avant l’annonce
- 🔕 peut désactiver l’annonce vocale (cloche uniquement)
- 🏰 peut jouer la mélodie Westminster à 12 heures

Le résultat est un effet élégant et discret, idéal pour la maison ou le bureau.

## ✨ Fonctionnalités principales

### 🕑 Annonce automatique de l’heure
- chaque heure (xx:00)
- chaque demi-heure (xx:30) – optionnel

### 🌐 Support multilingue automatique
- Italien 🇮🇹
- Anglais 🇬🇧
- Français 🇫🇷
- Allemand 🇩🇪 (avec gestion correcte de « halb »)
- Espagnol 🇪🇸

repli automatique vers l’italien

### ⏱️ Plage horaire configurable
- ex. uniquement de 8:00 à 22:00

###  🔔 Cloche optionnelle
- 🎵 12 sons prédéfinis au choix
- 🎶 possibilité d’utiliser un fichier audio personnalisé
- 🔕 son de notification Alexa « announce » (par défaut)

### 🧪 Fonction de test
- pour tester immédiatement l’annonce

### 🎯 Comportement

**Cloche (Chime) :**
- **Préréglages disponibles** : 12 sons dont church-bell, simple-bell, clock-chime, etc.
- **Son personnalisé** : Sélectionnez « custom » et entrez le chemin de votre fichier audio
- **Par défaut** : Son « announce » d’Alexa (si rien n’est sélectionné)
- **Désactivé** : Désactivez « use_chime » pour aucun son avant l’annonce

**Mélodie Westminster (Tower Clock) :**
- Option séparée « tower_clock »
- Joue **uniquement à 12:00** (midi)
- Remplace la cloche normale à cette heure

**Annonce vocale :**
- **Activée** (par défaut) : Alexa annonce l’heure après la cloche
- **Désactivée** : Cloche uniquement, aucune annonce vocale

**Annonces à la demi-heure :**
- **Activées** (par défaut) : Annonces à :00 et :30
- **Désactivées** : Annonces uniquement à :00

## ⚙️ Fonctionnement

Le cœur du système est la classe :

class DigitalPendulum

qui :
- s’enregistre sur un minuteur interne synchronisé (chaque minute à la seconde :00)
- vérifie :
  - si l’intégration est activée
  - si l’heure est dans la plage autorisée
  - si la minute est :00 (ou :30 si activé)
- construit le texte parlé selon la langue
- joue la cloche (si activée)
- envoie l’annonce vocale à l’appareil Alexa (si activée)

## 🗣️ Gestion des langues

La langue est détectée automatiquement depuis :

self.hass.config.language

Exemples d’annonces :

| Langue | Heure | Annonce |
|------|------|--------|
| 🇮🇹 IT | 10:30 | Ore 10 e trenta |
| 🇬🇧 EN | 14:00 | It's 14 o'clock |
| 🇫🇷 FR | 9:30 | Il est 9 heures trente |
| 🇩🇪 DE | 16:30 | Es ist halb 17 |
| 🇪🇸 ES | 11:00 | Son las 11 |

## 🔔 Cloche (signal initial)

Si l’option use_chime est activée :
- le son de notification Alexa ou le son sélectionné est joué
- le système attend 1,2 seconde
- l’annonce vocale démarre (si activée)

Cela crée un effet similaire à un véritable pendule 🎶.

## 🧩 Options de configuration

| Option | Description |
|------|------------|
| player | Appareil Alexa cible |
| start_hour | Heure de début |
| end_hour | Heure de fin |
| enabled | Activer/désactiver le pendule |
| announce_half_hours | Activer les annonces à la demi-heure (sinon seulement chaque heure) |
| voice_announcement | Activer/désactiver l’annonce vocale |
| tower_clock | Activer la mélodie Westminster à 12:00 |
| use_chime | Activer/désactiver la cloche avant l’annonce |
| preset_chime | Sélection du son de cloche (12 préréglages disponibles) |
| custom_chime_path | Chemin du son personnalisé |

Valeurs par défaut :

- ⏰ start_hour → 8
- ⏰ end_hour → 22
- 🔔 use_chime → True
- 🗣️ voice_announcement → True
- ⏰ announce_half_hours → True
- 🏰 tower_clock → False
- ✅ enabled → True

## 🧪 Test immédiat

Une méthode de test manuel est disponible :

async_test_announcement()

Qui :
- lit l’heure actuelle
- génère une phrase complète (ex. « Ore 15 e 42 »)
- la joue immédiatement sur l’appareil Alexa  

Utile pour vérifier : langue, volume, cloche, bon fonctionnement du TTS

## 📦 Prérequis

> ✨ **Disponible sur HACS** – installation et mises à jour simplifiées !

- 🏠 Home Assistant 2024.1.0 ou supérieur
- 🔊 Alexa Media Player installé et fonctionnel
- 📡 Appareil Alexa configuré comme lecteur


## 🎯 Utilisation idéale

- ✔️ Maisons intelligentes
- ✔️ Bureaux
- ✔️ Espaces communs
- ✔️ Effet « pendule moderne »
- ✔️ Rappel du temps non intrusif

## 🚀 Évolutions futures possibles

- ⏳ Annonces toutes les 15 minutes
- 🔇 Volume nocturne automatique
- 🗓️ Annonce du jour
- 📣 Support d’autres TTS

---
## 

## ☕ Soutenir le projet

Vous aimez ce projet ? S’il vous est utile, offrez-moi un café virtuel pour soutenir les évolutions futures ! Chaque petite contribution est grandement appréciée. 🙏

**Digital Pendulum est et restera toujours gratuit et open source.** Les dons sont entièrement volontaires ! ❤️


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/dregi56)

💡 **Vous préférez d’autres méthodes ?** Vous pouvez utiliser :

[![revolut](https://img.shields.io/badge/Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/egidio5t9d)
