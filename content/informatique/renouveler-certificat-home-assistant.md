---
title: "Configurer HTTPS pour Home Assistant"
url: /itech/crt_management/renewCertForHaOs/
description: "Créer et renouveler un certificat Let's Encrypt avec Nginx Proxy Manager."
weight: 30
---

## Prérequis

- Home Assistant OS opérationnel ;
- un domaine géré par OVH ;
- les identifiants de l’API OVH.

## 1. Installer Nginx Proxy Manager

1. installer l’extension [Nginx Proxy Manager](https://github.com/hassio-addons/addon-nginx-proxy-manager) ;
2. démarrer l’extension ;
3. ouvrir l’interface sur `http://ADRESSE_IP:81`.

![Accueil de Nginx Proxy Manager](/assets/images/renewCertForHaOs/2026-02-17_21-40.png)

## 2. Ajouter le certificat

1. ouvrir **SSL Certificates** ;
2. choisir **Add SSL Certificate → Let's Encrypt** ;
3. saisir le domaine ;
4. activer le challenge DNS ;
5. choisir OVH et renseigner les identifiants API ;
6. accepter les conditions, puis enregistrer.

![Configuration du challenge DNS OVH](/assets/images/renewCertForHaOs/2026-02-17_21-55.png)

## 3. Configurer le proxy

1. ouvrir **Hosts → Proxy Hosts** ;
2. créer ou modifier le proxy Home Assistant ;
3. sélectionner le certificat dans l’onglet **SSL** ;
4. activer **Force SSL** ;
5. enregistrer et tester l’URL HTTPS.

![Liste des proxys](/assets/images/renewCertForHaOs/2026-02-17_21-41.png)

![Actions sur le certificat](/assets/images/renewCertForHaOs/2026-02-17_21-42.png)

## Checklist

- [ ] Extension démarrée
- [ ] Challenge DNS OVH validé
- [ ] Certificat affecté au proxy
- [ ] Redirection HTTPS active
- [ ] Accès externe testé
