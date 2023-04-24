# Argumentation-based-multi-agent

## Description de la méthode 

### Architecture générale

Le projet a pour vocation de concevoir et développer un système multi-agent qui simule un débat sur un sujet spécifique entre deux agents. Toutefois, les agents ont des préférences différentes en matière de critères de sélection, ce qui crée des conflits lors de leur interaction. L'objectif du projet est donc de concevoir un système de dialogue entre les agents, tout en cherchant à déterminer si ces derniers seront capables de parvenir à un accord sur un élément spécifique. Pendant le débat, les agents construisent leur argumentation en utilisant des critères pertinents pour chaque élément discuté. 


### Notre histoire

Pour ce projet et pour aborder le problème, nous avons longtemps hésité sur quel sujet faire débattre nos agents. Devrions nous les faire débattre sur quel est le meilleur film ? Quel est le meilleur super héro ? Ou quel est le meilleur moteur ? Dans notre hésitation et sans parvenir à nous mettre d'accord, nous avons décidé d'utiliser ce projet pour nous aider à choisir un thème à choisir. Ainsi nous avons défini une trentaine de thème, et nous avons donné à chacun de ces thèmes un score aléatoire entre 0 et 10 pour chacun des 5 critères : 

* PERSONNAL INTEREST : Est-ce que le sujet est passionnant pour l’agent
* ORIGINALITY : Est-ce que le sujet est original
* CONTROVERSE : Est-ce que le sujet est controversé
* SUBJECT KNOWLEDGE : à quel point l'agent connaît bien le sujet
* AMOUNT OF WORK : Quantité de travail en plus. Par exemple, pour le thème philosophie, choisir ce sujet impliquerait un travail de recherche de thèses philosophiques. 

Les agents sont donc nous : Karim et Leila, et il débattent sur quel est le meilleur sujet pour le projet du cours de SMA ! Évidement parmi les thèmes sur lesquels ils argumentent, le même thème que le notre leur est proposé (celui de laisser les agents qu'ils vont construire, choisir le sujet).

### Définition de l’architecture

Agents et base de connaissance : Dans notre projet il y a donc 2 agents, Karim et Leila, ils ont chacun un nom, un fichier csv de préférences dans lequel les scores de chaque critère pour chaque item est différent. Nos 2 agents ont donc une base de connaissance différentes. Et ils évoluent tout deux dans l'environnement d'argumentation. 

Argumentation : La discussion se déroule de la manière suivante : 

1. Le premier agent propose un de ses 5 sujets préféré au 2eme.  
2. Deux cas : 
    * Si cet élément fait parti du top 5% des items préférés de l'agent 2, il accepte la proposition, ils commit tous les 2 et la discussion se termine ici, Ils se sont donc mis d'accord sur un sujet.
    * Sinon, le 2eme agent demande au premier pourquoi un tel choix ? 

3. Ici l'argumentation commence, et l'agent 1 donne son critère qui soutient le mieux son item.
4. L'agent2 reçoit cette argumentation et ici 3 cas se posent : 

    * Soit il propose un autre item qui, pour ce critère en question a un très bon score. Donc un meilleur item pour ce critère en question 
    * S'il ne trouve pas d'autre item qui soit meilleur pour ce critère en question il propose de diriger la discussion sur un autre critère pour cet item donné, critère que lui considère le plus important à discuter pour cet item donné
    * S'il ne trouve pas un autre critère, il en choisit juste un random parmi les 4 critères restants. 

5. Ensuite la discussion se poursuite en fonction de ce qu'il s'est passé à l'étape précédente : 

     * Si un nouvel item est proposé et que pour l'agent1 ce nouvel item fait parti du top 10 pourcent, il accepte, ils commit et la discussion se termine. 
     * Sinon les 2 derniers point de réitère avec inversion des agent1 et agent2 pour la proposition et l'argumentation. 

6. Dans le cas ou l'agent ne parvient pas à trouver un élément avec un critère supérieur, il propose un autre critère. 


## Analyses et Résultats

###Possible fin 

Ainsi pour cette simulation, il existe plusieurs fin possible :
* Soit les 2 agents se mettent d’accord sur un thème et ils pourront donc faire leur projet de SMA
* Soit les 2 agents n'arrivent pas à se mettre d'accord et la simulation se termine sur un désaccord au bout de 20 steps. Néanmoins il arrive que ce désaccord soit lié à une situation ou les 2 agents entament un dialogue de sourd. En effet, dans cette situation les 2 se fixent sur un critère spécifique et chacun propose le même item et cela en boucle. 


### Statistiques
Pour un nombre de steps = 20, nous avons effectués : 
* 50 itérations du cas ou l'agent Karim commence la discussion. On observe que dans plus de la moitié des cas les agents parviennent à s'accorder sur un sujet, même si ils leur arrive dans presque 1/3 des cas de conduire à un désaccord au bout de 20 steps. 

* 50 itérations du cas ou l'agent Leila commence la discussion. 
Ici les résultats sont assez surprenants, les agents n'arrive jamais à se mettre d'accord sur un sujet quand c'est l'agent Leila qui commence. 


## Conclusion
Ainsi pour ce projet, nous avons pu mettre en communication deux agents qui ont argumenté et débattu avec différents points de vue. L'étape suivante serait la nécessité d'ajouter une gestion de conflit pour gérer les divergences de croyances entre les agents. Cette évolution permettrait d'optimiser les échanges et de renforcer la pertinence des résultats obtenus.
