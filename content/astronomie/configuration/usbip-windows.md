---
title: "Connecter un périphérique USB à WSL"
url: /usbIpOnWindows/
description: "Rendre un périphérique USB Windows accessible dans WSL avec USB/IP."
weight: 40
---

## Prérequis

- WSL installé ;
- `usbipd-win` installé sous Windows ;
- terminal PowerShell ouvert en administrateur.

## 1. Vérifier WSL

Dans WSL :

```bash
lsusb
```

Le périphérique cible ne doit pas encore apparaître.

## 2. Identifier le périphérique

Dans PowerShell :

```powershell
usbipd list
```

Noter son `BUSID`, par exemple `2-2`.

## 3. Partager et attacher le périphérique

Dans PowerShell administrateur :

```powershell
usbipd bind --busid 2-2
usbipd attach --wsl --busid 2-2
```

## 4. Contrôler dans WSL

```bash
lsusb
ls -l /dev/ttyUSB*
```

Résultat attendu : le périphérique apparaît dans `lsusb` et, pour un adaptateur série, un port tel que `/dev/ttyUSB0` est créé.

## Checklist

- [ ] Périphérique identifié dans PowerShell
- [ ] `BUSID` partagé
- [ ] Périphérique attaché à WSL
- [ ] Périphérique visible avec `lsusb`
- [ ] Port série présent, si applicable
