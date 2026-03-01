---
layout: default
title: Sauvegarde Kopia
permalink: /usbIpOnWindows/
---

# Utiliser le service UsbIp sur un OS Microsot 





# Console WSL (acte 1)

emmanuel@pc-salon:~$ lsusb
emmanuel@pc-salon:~$


Aucun équipement n'est vu. 😕

# Console Powershell

```bash
PS C:\Users\emman> usbipd list
Connected:
BUSID  VID:PID    DEVICE                                                        STATE
2-2    10c4:ea60  Silicon Labs CP210x USB to UART Bridge (COM3)                 Shared
2-3    062a:4102  Périphérique d’entrée USB                                     Not shared
2-10   0a5c:5842  Dell ControlVault w/o Fingerprint Sensor, Lecteur de cart...  Not shared
2-11   0bda:58fd  Integrated Webcam                                             Not shared
2-14   8087:0029  Intel(R) Wireless Bluetooth(R)                                Not shared
Persisted:
GUID                                  DEVICE
96b8bb34-afb9-4e5e-963d-37236c65061b  Silicon Labs CP210x USB to UART Bridge (COM3)
```

Repérer l'équipement cible et son BusID puis lancer:
```bash
PS C:\Users\emman> usbipd attach --wsl --busid 2-2
```

# Console WSL (acte 2)
```
emmanuel@pc-salon:~$ lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 10c4:ea60 Silicon Labs CP210x UART Bridge
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
emmanuel@pc-salon:~$
emmanuel@pc-salon:~$ ls /dev/ttyUSB0
/dev/ttyUSB0
emmanuel@pc-salon:~$
```

