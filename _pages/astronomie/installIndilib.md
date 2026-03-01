---
layout: default
title: Sauvegarde Kopia
permalink: /installIndilib/
---


# Compiler indlib (sous ubuntu 24.04)
 Vérification de la distribution installée
root@indiserver:~# cat /etc/*release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04.1 LTS"
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.1 LTS (Noble Numbat)"
VERSION_CODENAME=noble
.....


 

 # Installation des dépendances
root@indiserver:~#apt install -y git cdbs dkms cmake fxload \
 libev-dev libgps-dev libgsl-dev libraw-dev \
 libusb-dev zlib1g-dev libftdi-dev libjpeg-dev\
 libkrb5-dev libnova-dev   libtiff-dev \
 libfftw3-dev librtlsdr-dev  libcfitsio-dev \
 libgphoto2-dev   build-essential \ 
 libusb-1.0-0-dev libdc1394-dev \
 libboost-regex-dev libcurl4-gnutls-dev \
 libtheora-dev


 
# Rapatriement et compilation des sources
```bash
root@indiserver:~# mkdir git
root@indiserver:~# cd git
root@indiserver:~# git clone --depth=1  https://github.com/indilib/indi indi-core
root@indiserver:~# git clone --depth=1  https://github.com/indilib/indi-3rdparty indi-3rd
```
 


Compilation de indi-core
root@indiserver:~# cd /root/git/indi-core
root@indiserver:~# rm -rf build && mkdir build
root@indiserver:~# cd build 
root@indiserver:~# cmake -DCMAKE_INSTALL_PREFIX=/usr \
-DCMAKE_BUILD_TYPE=Debug /root/git/indi-core
root@indiserver:~# make -j$(nproc)
root@indiserver:~# make install


Compilation de indi-3rd (driver optionnel)
root@indiserver:~# cd /root/git/indi-3rd
root@indiserver:~# rm -rf build && mkdir build
root@indiserver:~# cd build 
root@indiserver:~# cmake -DCMAKE_INSTALL_PREFIX=/usr \
-DCMAKE_BUILD_TYPE=Debug /root/git/indi-3rd
root@indiserver:~# make -j$(nproc)
root@indiserver:~# make install

 

Si des modules posent soucis à la compilation (ex astroasis), commenter les lignes y faisant référence dans le fichier CMakeLists.txt



Les règles udev (montage fixe)
 

root@indiserver:~# lsusb 
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 2341:0043 Arduino SA Uno R3 (CDC ACM)
Bus 001 Device 005: ID 05e3:0610 Genesys Logic, Inc. Hub
Bus 001 Device 006: ID 1546:01a7 U-Blox AG [u-blox 7]
Bus 001 Device 007: ID 05e3:0610 Genesys Logic, Inc. Hub
Bus 001 Device 008: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port / Mobile Phone Data Cable
Bus 001 Device 009: ID 04a9:327f Canon, Inc. EOS Rebel T5 / EOS 1200D / EOS Kiss X70
Bus 001 Device 010: ID 15a2:a50f Freescale Semiconductor, Inc. Celestron Focuser
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 002 Device 002: ID 05e3:0626 Genesys Logic, Inc. Hub
Bus 002 Device 003: ID 05e3:0626 Genesys Logic, Inc. Hub
Bus 002 Device 004: ID 03c3:120d ZWO ASI120MM-S
root@indiserver:~# 


root@indiserver:~# cat /etc/udev/rules.d/99-astro_devices.rules 
SUBSYSTEM=="tty", ATTRS{idVendor}=="15a2", ATTRS{idProduct}=="a50f", \
SYMLINK+="astro_celestron_focuser", MODE="0666"

SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", \
SYMLINK+="astro_celestron_mount_avx", MODE="0666"

SUBSYSTEM=="usb", ATTRS{idVendor}=="04a9", ATTRS{idProduct}=="327f", \
SYMLINK+="astro_canon_1200d", MODE="0666"
 
SUBSYSTEM=="usb", ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a7", \
SYMLINK+="astro_dongle_gps", MODE="0666"


root@indiserver:~# udevadm control --reload
root@indiserver:~# udevadm trigger

IndiServer : creation d'un service
🟥 Recommandé uniquement si la configuration est figée.

root@indiserver:~# cat /etc/systemd/system/indi.service 
[Unit]
Description=INDI Server for astronomical devices
After=network.target

[Service]
ExecStart=/usr/bin/indiserver /usr/bin/indi_celestron_gps \
/usr/bin/indi_celestron_sct_focus /usr/bin/indi_canon_ccd \
/usr/bin/indi_asi_ccd /usr/bin/indi_joystick /usr/bin/indi_gpsd
User=root  
Restart=on-failure

[Install]
WantedBy=multi-user.target


root@indiserver:~# systemctl start indi.service
root@indiserver:~# systemctl status indi.service
root@indiserver:~# systemctl enable|disable indi.service (activer ou non au boot)
IndiServer: démarrage manuel
root@indiserver:~#  /usr/bin/indiserver -v /usr/bin/indi_celestron_gps \
/usr/bin/indi_celestron_sct_focus /usr/bin/indi_canon_ccd \
/usr/bin/indi_asi_ccd /usr/bin/indi_joystick /usr/bin/indi_gpsd



