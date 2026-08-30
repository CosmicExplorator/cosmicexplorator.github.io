---
title: "Créer un serveur INDI distant"
url: /installIndilib/
description: "Compiler INDI sous Ubuntu 24.04 et créer un serveur distant."
weight: 10
---

[![Projet INDI](/assets/images/installIndilib/2026_03_01-logo.png)](https://indilib.org)

## Prérequis

- Ubuntu 24.04 ;
- accès `root` ;
- périphériques USB connectés pour créer les règles `udev`.

## 1. Installer les dépendances

```bash
apt update
apt install -y \
  build-essential cdbs cmake dkms fxload git \
  libboost-regex-dev libcfitsio-dev libcurl4-gnutls-dev \
  libdc1394-dev libev-dev libfftw3-dev libftdi-dev \
  libgphoto2-dev libgps-dev libgsl-dev libjpeg-dev \
  libkrb5-dev libnova-dev libraw-dev librtlsdr-dev \
  libtheora-dev libtiff-dev libusb-1.0-0-dev libusb-dev zlib1g-dev
```

## 2. Télécharger les sources

```bash
mkdir -p /root/git
cd /root/git
git clone --depth=1 https://github.com/indilib/indi indi-core
git clone --depth=1 https://github.com/indilib/indi-3rdparty indi-3rd
```

## 3. Compiler INDI Core

```bash
cmake -S /root/git/indi-core -B /root/git/indi-core/build \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_BUILD_TYPE=Release
cmake --build /root/git/indi-core/build --parallel
cmake --install /root/git/indi-core/build
```

## 4. Compiler les pilotes tiers

```bash
cmake -S /root/git/indi-3rd -B /root/git/indi-3rd/build \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_BUILD_TYPE=Release
cmake --build /root/git/indi-3rd/build --parallel
cmake --install /root/git/indi-3rd/build
```

Si un pilote optionnel échoue, désactiver uniquement sa cible CMake, puis relancer la compilation.

## 5. Créer les règles udev

Identifier les périphériques :

```bash
lsusb
```

Créer `/etc/udev/rules.d/99-astro_devices.rules` en adaptant les identifiants :

```udev
SUBSYSTEM=="tty", ATTRS{idVendor}=="15a2", ATTRS{idProduct}=="a50f", SYMLINK+="astro_celestron_focuser", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", SYMLINK+="astro_celestron_mount_avx", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="04a9", ATTRS{idProduct}=="327f", SYMLINK+="astro_canon_1200d", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a7", SYMLINK+="astro_dongle_gps", MODE="0666"
```

Recharger les règles :

```bash
udevadm control --reload
udevadm trigger
```

## 6. Tester manuellement

```bash
/usr/bin/indiserver -v \
  /usr/bin/indi_celestron_gps \
  /usr/bin/indi_celestron_sct_focus \
  /usr/bin/indi_canon_ccd \
  /usr/bin/indi_asi_ccd \
  /usr/bin/indi_joystick \
  /usr/bin/indi_gpsd
```

## 7. Créer le service systemd

À utiliser uniquement si la liste des pilotes est figée.

Créer `/etc/systemd/system/indi.service` :

```ini
[Unit]
Description=INDI Server for astronomical devices
After=network.target

[Service]
ExecStart=/usr/bin/indiserver /usr/bin/indi_celestron_gps /usr/bin/indi_celestron_sct_focus /usr/bin/indi_canon_ccd /usr/bin/indi_asi_ccd /usr/bin/indi_joystick /usr/bin/indi_gpsd
User=root
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now indi.service
systemctl status indi.service
```

## Checklist

- [ ] INDI Core compilé et installé
- [ ] Pilotes nécessaires installés
- [ ] Liens `udev` présents
- [ ] Démarrage manuel réussi
- [ ] Port INDI `7624` accessible
- [ ] Service systemd actif, si utilisé
