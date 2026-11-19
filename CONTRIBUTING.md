__Combien de relecteurs par pull request ? Que se passe-t-il quand le seul relecteur compétent est absent ?__
1 validation par pull request par l’autre membre de l'équipe dev, on attend sa disponibilité si absence, on ne force pas la validation de la pull request, afin de ne pas compromettre la version de production.

__Conventions de nommage des branches et des messages de commit.__
On nomme les branches en “dev-nomdudev”. 
On nomme les commits en format “[0.0.0] commit” en français. (voir partie “Versionnage” pour précision sur le code de version)

__Definition of Done : à quel moment une tâche est-elle « terminée » ?__
On peut dire qu’une tâche est terminée, lorsque tous les tests précédemment créés, et les nouveaux tests couvrant l’entièreté de la nouvelle fonctionnalité ont été validés et que son déploiement est effectué.

__Versionnage : comment savoir en 10 secondes quelle version tourne en production ?__
style : 0.0.0 
le premier 0 = version principal du projet
le 2eme 0 = feature de la branche en cours
le 3eme = fix de la branche en cours
chaque dev sur sa branche et censé être sur le même premier 0 commun avec le reste de l’équipe, ensuite sur sa branche il avance et versionné selon la feature qu’il vient d'implémenter ou le fix appliqué. Une fois que tout les devs on fini ce qu’il avait à faire : push_request -> merge ce qui mène à l’incrémentation du premier 0

Nommer les version ex: V1.2.23


__Secrets : où vivent-ils, qui y a accès, que fait-on le jour où l’un d’eux fuit ?__
Ils sont dans une partie chiffrée du dépôt (gitHub secrets and variables).
Seuls le chef de projet et ceux autorisés possèdent un accès de gestion. 
On révoque le secret, on en génère un nouveau et on vérifie les logs pour vérifier toutes actions frauduleuses avec l’ancien secret. On fait un état des lieux pour savoir ce qui à pu être compromis, et on agit en fonction (base de données CNIL, code du serveur => redéploiement)

__Pourquoi on ne push pas sur la branche main__
Car main est la branche de prod, les fonctionnalités sont ajoutées sur des branc
hes dev-<nom du dev>.
	
__Ne pas mettre le .env en public__
Cela peut compromettre des données importantes.

__Traduisez ensuite dans GitHub ce qui peut l’être. Faites des captures de la configuration dans docs/config/. Signalez explicitement les règles qui ne peuvent pas être imposées par l’outil et qui reposent sur la discipline de l’équipe?__

Github : Relecteurs pull request, nommages branches, secrets, definition of done, .env dans le gitignore.
Discipline équipe : Nom des commits, versionnage 

![règle des branches](./docs/img/regle_branche.png)
![règle des branches 2](./docs/img/regle_2.png)


__Règle__: Sur Main on restreint les suppressions et on bloque les push et force push, 
__Raison__: car main est censé être la prod les fonctionnalités sont ajoutées sur des branches (dev).

__Règle__: Adapter le développement aux revues de code.
__Raison__: Car sinon il peut y avoir un ralentissement avec trop peu de reviewers.

__Règle__: Ne pas mettre le .env en public.
__Raison__: Cela peut compromettre des données importantes.

__Règle__: Tester intégralement chaque fonctionnalité avant déploiement.
__Raison__: Afin d’avoir une branche main stable et fonctionnelle.
