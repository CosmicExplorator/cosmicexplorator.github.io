# Renouvellement Automatique d'un certificat Let's Encrypt sur Synology

Voici la procédure que j'utilise pour renouveler automatiquement un certificat
Let's Encrypt via acme.sh et OVH DNS.


## 0. Rapatriement sur DSM

```
curl https://raw.githubusercontent.com/acmesh-official/acme.sh/master/acme.sh | sh -s -- --install-online --accountemail  "contact@gmail.com" --nocron
```

## 1. Préparer les variables OVH

Créer un fichier `ovh.ini` :
```bash
cat ovh.ini
# Informations pour l'accès à l'API OVH
export OVH_AK="xxxxx"
export OVH_AS="xxxxx"
export OVH_CK="xxxxx"
```
## 2. Générer le certificat

```bash
source /var/services/homes/emmanuel/.acme.sh/ovh.ini
/var/services/homes/emmanuel/.acme.sh/acme.sh --issue -d  mydomain.ovh --dns dns_ovh --server letsencrypt
```

## 3. Déployer sur Synology

```bash
source /var/services/homes/emmanuel/.acme.sh/ovh.ini
/var/services/homes/emmanuel/.acme.sh/acme.sh --deploy --home /var/services/homes/emmanuel/.acme.sh/ -d "mydomain.ovh" --deploy-hook synology_dsm --debug 3
```


## 4. Automatiser

Créer une tâche planifiée dans DSM.
