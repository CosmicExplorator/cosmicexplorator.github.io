# Huawei HiLink SMS

Cette application affiche la boîte SMS d'un modem Huawei HiLink et permet
d'envoyer ou supprimer des messages depuis Home Assistant.

## Configuration

- `modem_url` : adresse de l'interface HiLink, généralement `http://192.168.8.1/`.
- `username` et `password` : identifiants facultatifs du modem.
- `max_messages` : nombre maximal de messages lus dans chaque boîte.

Après le démarrage, activez **Afficher dans la barre latérale** sur la page de
l'application. Home Assistant ouvre alors l'interface par Ingress, sans exposer
de port sur le réseau local.

## Dépannage

La machine Home Assistant doit pouvoir joindre l'adresse du modem. Si la boîte
reste vide, ouvrez les journaux de l'application et vérifiez que l'interface
HiLink est accessible depuis le réseau de Home Assistant.

