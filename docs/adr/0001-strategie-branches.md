__Proposez une stratégie de gestion de vos branches (quelles branches ? qui ? comment) :__
Branche main protégée, aucun push autorisé, requis une pull request pour merge, cette pull request doit être validé par 1 personnes membre de l'équipe dev. Les suppression push et force push sont restreintes. Cette règle permet de conserver une version de production sur le main qui est fonctionnelle en tout temps.  
<br>

__Expliquer comment un correctif urgent arrive en production avec votre stratégie, et comment il revient dans le travail en cours :__
Grâce aux règles de versioning on peut avoir un suivi complet (voir T3), pour déployer un patch urgent en prod on versionnera le push et on procédera au test avant via docker, github action.
<br>

__Indiquer à quel signal vous sauriez que ce choix ne fonctionne plus :__ 
Quand des push sont envoyés sur main trop régulièrement, que les pull request cause des bugs et que la production tombe en panne.
