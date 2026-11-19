__Proposez une stratégie de gestion de vos branches (quelles branches ? qui ? comment) :__
Branche main protégée, aucun push autorisé, requis une pull request pour merge, cette pull request doit être validé par 1 personnes membre de l'équipe dev. Les suppression push et force push sont restreintes. Cette règle permet de conserver une version de production sur le main qui est fonctionnelle en tout temps.  
<br>

__Expliquer comment un correctif urgent arrive en production avec votre stratégie, et comment il revient dans le travail en cours :__
Grâce aux règles de versioning on peut avoir un suivi complet (voir T3), pour déployer un patch urgent en prod on versionnera le push et on procédera au test avant via docker, github action.
<br>

__Indiquer à quel signal vous sauriez que ce choix ne fonctionne plus :__ 
Quand des push sont envoyés sur main trop régulièrement, que les pull request cause des bugs et que la production tombe en panne.

__Cririque :__
La mise en pratique de notre stratégie de branche nous à montré un problème significatif. Lorsque l'on nomme nos commit x.x.x pour versionner nos changements, les messages de commits sont confus sur la branche main et dev. On a par exemple 1.4.0 et 1.1.0 avec 1.1.0 qui est commit après. Notre versionnage avec la version, devrait être effectuée uniquement lors des messages de commit pour les Pull Request. 
