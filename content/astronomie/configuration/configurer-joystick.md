---
title: "Partager un joystick avec USB/IP"
url: /configUseJoystick/
description: "Connecter à distance un joystick au serveur INDI avec USB/IP."
weight: 30
---

## Architecture

{{< mermaid >}}
flowchart LR
    J["Joystick"] --> S["Station cliente<br/>usbip-host"]
    S -->|"TCP 3240"| I["Serveur INDI<br/>vhci-hcd"]
    I --> E["Pilote INDI Joystick"]
{{< /mermaid >}}

## Prérequis

- Ubuntu sur les deux machines ;
- accès administrateur ;
- port TCP `3240` autorisé entre les machines ;
- joystick branché à la station cliente.

## 1. Préparer la station cliente

```bash
sudo apt install -y linux-tools-generic
sudo modprobe usbip-core
sudo modprobe usbip-host
```

Ajouter dans `/etc/modules-load.d/usbip.conf` :

```text
usbip-core
usbip-host
```

## 2. Identifier et exporter le joystick

```bash
sudo usbip list -l
```

Noter le `BUSID`, par exemple `3-6`, puis lancer :

```bash
sudo usbipd -D
sudo usbip bind --busid=3-6
```

Contrôler l’export :

```bash
usbip list --remote=127.0.0.1
```

Pour arrêter l’export :

```bash
sudo usbip unbind --busid=3-6
```

## 3. Automatiser l’export

Créer `/etc/systemd/system/usbip-export-joystick.service` en adaptant le `BUSID` :

```ini
[Unit]
Description=Export du joystick avec USB/IP
After=network-online.target
Wants=network-online.target

[Service]
Type=forking
ExecStart=/usr/sbin/usbipd -D
ExecStartPost=/usr/sbin/usbip bind --busid=3-6
ExecStop=/usr/sbin/usbip unbind --busid=3-6
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Vérifier les chemins avec `command -v usbip usbipd`, puis activer le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now usbip-export-joystick.service
sudo systemctl status usbip-export-joystick.service
```

## 4. Préparer le serveur INDI

```bash
sudo apt install -y linux-tools-generic
sudo modprobe vhci-hcd
```

Ajouter `vhci-hcd` dans `/etc/modules-load.d/usbip.conf`.

## 5. Attacher le joystick

Lister les périphériques exportés par la station :

```bash
usbip list --remote=ADRESSE_IP_STATION
```

Attacher le joystick :

```bash
sudo usbip attach --remote=ADRESSE_IP_STATION --busid=3-6
```

Contrôler :

```bash
usbip port
lsusb
```

Pour le détacher :

```bash
sudo usbip detach --port=0
```

## 6. Activer le joystick dans INDI

1. ajouter `/usr/bin/indi_joystick` au profil INDI ;
2. redémarrer le profil ;
3. connecter KStars au serveur ;
4. ouvrir l’onglet **Joystick** dans Ekos ;
5. tester un mouvement à faible vitesse.

## Checklist

- [ ] Joystick visible avec `usbip list -l`
- [ ] Périphérique exporté sur la station
- [ ] Port TCP `3240` accessible
- [ ] Joystick attaché sur le serveur
- [ ] Joystick visible avec `lsusb`
- [ ] Pilote `indi_joystick` chargé
- [ ] Axes testés à faible vitesse
