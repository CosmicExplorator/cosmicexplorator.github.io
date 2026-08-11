---
title: "indi-ansible"
description: "Déployer et configurer un serveur INDI avec Ansible."
weight: 30
---

[`indi-ansible`](https://github.com/CosmicExplorator/indi-ansible) automatise l’installation d’un serveur INDI sous Ubuntu 26.04.

Le projet permet notamment de :

- compiler et installer INDI et les pilotes nécessaires ;
- créer des règles udev stables pour les équipements astronomiques ;
- charger des profils matériels simples ou combinés ;
- configurer KStars/Ekos ;
- partager le GPS et le joystick avec USB/IP ;
- vérifier la présence du matériel avant de démarrer une session.

## Installation du socle

```bash
git clone https://github.com/CosmicExplorator/indi-ansible.git
cd indi-ansible
ansible-playbook site.yml
```

[Consulter le projet et les playbooks sur GitHub →](https://github.com/CosmicExplorator/indi-ansible)
