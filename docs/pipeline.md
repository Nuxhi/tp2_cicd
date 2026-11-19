# T4 — Conception du pipeline 


### 1\. un schéma du pipeline de la PR jusqu’à la production, avec les points d’approbation humaine ;


Schéma Mermaid : 
```
flowchart TD
A\[PR ouverte depuis dev-nom] --> B\[CI : lint + tests + build image sans push]
B -->|échec| A B -->|OK| C{{Relecture : 1 approbation 👤}} 
C --> D\[Merge dans main] 
D --> E\[Build + push GHCR : tag vX.Y.Z + sha] 
E --> F\[Déploiement STAGING auto]
F --> G\[Smoke test : /health + GET /products] 
G -->|échec| X\[Stop, prod inchangée] G -->|OK| H{{Approbation prod 👤 environment protégé}} 
H --> I\[Déploiement PROD] I --> J\[Healthcheck post-déploiement] 
J -->|échec| R\[Retour arrière auto vers version précédente] 
J -->|OK| K\[Release GitHub + tag] 

``` 



### 2\. un tableau avec, pour chaque étape : son déclencheur, sa durée estimée, si elle est bloquante ;



|**Étape**|**Déclencheur**|**Durée estimée**|**Bloquante**|
|-|-|-|-|
|Lint + Tests|PR ouverte ou mise à jour|1-2 Min|Oui (Check requis)|
|Build images (sans Push)|PR|2-3 Min|Oui|
|Relcture humaine|PR prête|Variable (objectif > 4h) |Oui|
|Build + Push GHCR|Merge sur main|2-3 Min|Oui|
|Déploiement staging|Fin du push|1 Min|Oui|
|Smoke test staging|Fin de deploiement|30 Sec|Oui|
|Approbation prod|Smoke test ok|Variable|Oui|
|Déploiement prod + healthcheck|Approbation|1-2 Min|Oui (déclenche le rollback)|







### 3\. la procédure de retour arrière : qui la déclenche, comment, en combien de temps, et ce qu’elle ne sait pas annuler


Un des devs qui la déclenche.

Arrêtez le serveur, faites un retour en arrière de version. La durée peut varier

Les fuites de données ne peuvent être annulées.



