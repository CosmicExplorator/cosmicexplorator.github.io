# Installation dans Home Assistant

1. Copier `custom_components/huawei_sms` dans `/config/custom_components/`.
2. Copier `www/huawei-sms-card.js` dans `/config/www/`.
3. Ajouter le capteur dans `/config/configuration.yaml` :

   ```yaml
   sensor:
     - platform: huawei_sms
       name: SMS Huawei E3372
       url: http://192.168.8.1/
       max_messages: 20
       country_code: "+33"
   ```

   Si l'interface HiLink est protégée, ajouter `username` et `password` en utilisant
   de préférence `secrets.yaml`.

4. Exclure le capteur de Recorder :

   ```yaml
   recorder:
     exclude:
       entities:
         - sensor.sms_huawei_e3372
   ```

5. Vérifier la configuration, puis redémarrer Home Assistant.
6. Ajouter `/local/huawei-sms-card.js?v=5` comme ressource JavaScript de type module.
7. Créer une vue `SMS` dans le tableau de bord. En mode YAML, copier le
   contenu de `lovelace/sms-view.yaml` dans la liste `views`. Depuis l'éditeur
   graphique, créer la vue puis ajouter une carte manuelle avec :

   ```yaml
   type: custom:huawei-sms-card
   entity: sensor.sms_huawei_e3372
   title: SMS et contacts SIM
   ```

   La section **Contacts SIM** contient les champs `Nom` et `+33612345678`
   ainsi que le bouton **Ajouter**.

Pour tester sans la carte, ouvrir **Outils de développement → Actions** :

```yaml
action: huawei_sms.add_contact
data:
  name: "Jean Dupont"
  phone_number: "+33612345678"
```

Le carnet SIM dépend du firmware HiLink. Si l'appel `pb-new` échoue, consulter les
journaux `custom_components.huawei_sms` et tester le carnet depuis l'interface web
du modem.
