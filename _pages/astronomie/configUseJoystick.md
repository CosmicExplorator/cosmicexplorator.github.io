---
layout: default
title: Sauvegarde Kopia
permalink: /configUseJoystick/
---



# Piloter une monture equatoriale avec un joystick
 
Architecture de l'observatoire
 
J'ai opté pour une solution qui permet de centraliser tous les périphériques "astro" sur le serveur indi. Le joystick connecter sur la station cliente, va être transmis au serveur via "ip". Ainsi le joystick sera vu comme étant directement connecté au serveur.
Pour cela nous utilisons le service usbipd.
 
 
Pré-requis:
Serveur indi et station cliente sont sur des distributions linux Ubuntu

```bash
root@station:~# cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.1 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
```
  
# Configuration station (reliée au joystick)
## Installation du service usbip
```bash
root@station:~#sudo apt install -y linux-tools-generic
root@station:~# sudo modprobe usbip-core
root@station:~# sudo modprobe usbip-host
```

## Activation des modules
```bash
root@station:~# echo -e "usbip-core\nusbip_common_mod\nusbip-host" | \
sudo tee /etc/modules-load.d/usbip.conf > /dev/null
```

## Recherche du joystick
```bash
root@station:~# sudo usbip list -l
 - busid 3-12 (8087:07dc)
   Intel Corp. : Bluetooth wireless interface (8087:07dc)

 - .......
   .......

 - busid X-Y (06a3:0c28)        <===== le joystick est reconnu (noté: X-Y)
   Saitek PLC : unknown product (06a3:0c28)
root@station:~# BUSID=$(usbip list -l | grep -B1 "06a3:0c28" | grep "busid" |\
sed -E 's/.*busid ([0-9-]+).*/\1/');
root@station:~# echo "$BUSID"
```

## Démarrage du service (manuellement)
```bash
root@station:~# sudo usbipd -D 
```

## Creation d'un service (automatique)
```bash
root@station:~# bash -c 'cat > /etc/systemd/system/usbip.service <<EOF
[Unit]
Description=Exports USB device over IP
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
Restart=on-failure
User=root
Group=root
ExecStart=/usr/lib/linux-tools/$(uname -r)/usbipd
ExecStartPost=/bin/bash -c "sleep 2 && /usr/lib/linux-tools/$(uname -r)/usbip bind --busid=X-Y"
ExecStop=/usr/lib/linux-tools/$(uname -r)/usbip unbind --busid=X-Y

[Install]
WantedBy=multi-user.target
EOF'

# Recharger systemd pour prendre en compte le nouveau service
root@station:~#systemctl daemon-reload

# Activer le service pour qu'il démarre automatiquement au boot
root@station:~#systemctl enable usbip.service

# Démarrer immédiatement le service
root@station:~#systemctl start usbip.service

# Vérifier son état
root@station:~#systemctl status usbip.service
```

 

## Liaison du périphérique  (manuellement)
```bash
sudo usbip bind -b 3-6
```
## Coupure du périphérique (manuellement)
```bash
sudo usbip unbind -b 3-6
```


# Configuration du serveur qui héberge  indiserver
## Installation du service usbip
```bash
root@indiserver:~#sudo apt install -y linux-tools-generic
root@indiserver:~#  sudo modprobe vhci-hcd
Creation d'un service dédié

root@indiserver:~#cat 
[Unit]
Description=USB/IP Daemon
Requires=network-online.target
After=network-online.target


[Service]
Type=simple
Restart=on-failure
User=root
Group=root
ExecStart=/usr/lib/linux-tools/6.11.0-17-generic/usbipd
#ExecStartPost=/usr/lib/linux-tools/6.11.0-17-generic/usbip bind --busid=8-1
ExecStop=/usr/lib/linux-tools/6.11.0-17-generic/usbip unbind

[Install]
WantedBy=multi-user.target

root@indiserver:/etc/systemd/system# sudo systemctl start usbip
root@indiserver:/etc/systemd/system# sudo systemctl status usbip
root@indiserver:/etc/systemd/system# sudo systemctl stop usbip
root@indiserver:/etc/systemd/system# sudo systemctl enable usbipd
```

## Détruire les process (usbip) existant sur le port 3240
```bash
root@indiserver:/etc/systemd/system# sudo kill -9 $(sudo lsof -t -i :3240)
```

## Démarrage du service (manuellement)
```bash
root@indiserver:~# sudo usbipd -D 
```
## Connexion au périphérique (relevé l'@IP de la station)
```bash
root@indiserver:~# sudo usbipd -D
root@indiserver:~# sudo usbip attach -r @ip_station -b X-Y
```
vérification que le joystick est vu comme équipement USB sur le server
```bash
root@indiserver:~# lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
........
Bus 003 Device 002: ID 06a3:0c28 Saitek PLC Aviator for Playstation 3/PC  <==== :)
```


Il ne reste plus qu'à relancer le server indi avec ce nouvel équipement
```bash
root@indiserver:~# indiserver /usr/bin/indi_celestron_gps /usr/bin/indi_\
celestron_sct_focus /usr/bin/indi_canon_ccd  /usr/bin/indi_joystick 
```
Ensuite, kstars (sur la station) après s'être connecté au serveur, proposera un nouvel onglet Joystick dans Ekos.

 



 Il est alors possible de contrôler la monture et le moteur de mise au point. Extra!
