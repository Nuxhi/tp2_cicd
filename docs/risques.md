1. _“ Les mots de passe et clés d’API étaient dans un fichier .env versionné. “_ :
Risque de sécurité : fuite des données, possible récupération des données de la base de données, possible compromission du serveur. 
Gravité : très élevé. Nous utilisons des secrets dans Github pour stocker nos variables d’environnement critiques. Le .env sera ajouté dans le .gitignore pour qu’il ne soit pas publié sur le dépôt. La gravité est très élevée, l’effort de mise en place est faible. 
<br>

2. _“ Les tests existaient à peine et personne ne les lançait.”_ + problème mois d'août :   
Risque d’organisation : le manquement des jeux de tests a paralysés le travail. Les pratiques des dev ont causé une perturbation du bon fonctionnement de l’application. Gravité élevé : perte d’argents des établissement du au fonctionnement perturbé, perte de client possible. Dans notre version, les Github actions garantissent l'exécution des tests à chaque PR, les règles de codage nécessitent aux développeurs d’écrire des tests à chaque nouvelle feature. Gravité : élevée, l’effort de mise en place est élevé (couverture de code dans les tests, respect des conventions de code définies).
<br>

3. _“Les revues de code vont tout ralentir, on est trop peu nombreux.”_  
Risque d’organisation : Le développement des fonctionnalités doit être en accord avec la capacité de revue spécifiquement avec 2 développeurs, car sinon un des deux développeurs doit attendre que l’autre fasse une revue de son code et ne peut donc rien faire. La gravité est élevée car les deadlines peuvent ne plus être respectées. L'exécution systématique des tests peut empêcher de review des fonctionnalités qui ne fonctionnent pas entièrement, ce qui optimise le temps passé à faire des revues de code. 
Gravité : élevée, l'effort de mise en place des tests est élevé.
Finalement, les tests ont des impacts sur plusieurs risques.
<br>  

4. _“Tout le monde poussait directement sur la branche principale”_, _“un workflow construisait l’image avec le tag latest et la déployait sans tests en SSH à chaque push”_  
Risque de fiabilité : Écrasement du tag latest pose des problèmes pour connaitre la version exacte. Le manque de tests automatisés peut permettre à des fonctionnalités non vérifiées et donc potentiellement non fonctionnelles d'être déployé.
Risque d’organisation : Il faut utiliser des branches pour avoir une branche main stable et fonctionnelle et développer des fonctionnalités en parallèles de manière propre. 
Gravité : très élevée, l’application ne peut plus fonctionner, il est donc nécessaire d'empêcher le push sur main et d’utiliser les pull request il faut aussi maintenir un versionning défini.
La configuration de github, l'exécution automatique des tests ainsi que les conventions de codage mises en place permettent d’assurer d’avoir une version stable en production. 
Gravité très élevé et effort de mise en place moyen (config github et github actions).  
<br>  

5. _“Les restaurateurs réclament des améliorations assez souvent. On doit pouvoir livrer vite.”_
Risque d’organisation : Il faut que les cycles de développement soient bien respectés afin de pouvoir répondre aux demandes des clients et ne pas être ralenti. 
Gravité : Elevé, l’automatisation CI via github permet une mise en production rapide des nouvelles features après PR sur le main.
Gravité élevé et effort de mise en place moyen (config github actions).
