# PROJET : CONNEXION KAFKA À HIVE
-------------------------

## QUELQUES INFOS SUR LES TECHNOLOGIES UTILISÉES

* Utilisation de Kafka, comme plateforme distribuée de message utilisant le principe publish/subscribe.
- Pour plus d'information, voir : [dossier maitre des différents use-case kafka: ](https://gitbox.affini-tech.net/Affini-Tech/Kafka)

* Utilisation de Hive, comme base de données dans un environnement distribué. Les requêtes sont de type HQL (pour HiveQL).

* Utilisation de Twitter, comme principale source de données.

## LE PRINCIPE DE FONCTIONNEMENT:

Le but est d'insérer des données que nous recevons en flot continue dans Hive. Partons du principe que notre cluster Hadoop sous distribution Hortonworks est déjà installé et configuré. Nous disposons donc:
* D'un ou plusieurs brokers kafka géré(s) par Zookieper
* Un entrepôt de données Hive ainsi que sa vue dans Hortonworks



Nous devrons donc nous occuper:

* De la récupération en flot continue (stream) de tweets selon un # défini. (il s'agit ici d'un exemple: le client pourra selon son bon vouloir envoyer le type de message qu'il veut)
* De l'envoie de ces tweet dans les brokers kafka.
* Du stockage de ces messages par paquet de X messages (que l'on pourra définir)
* De l'envoie de ces messages dans Hive

* **Toute la configuration s'effectue dans le fichier *params.json* ainsi que *config.json* se trouvant dans le** **dossier /params**


![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/fonctionnement.png "fonctionnement Kafka")



### L'ARBORESCENCE DES FICHIERS:

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/arborescence.png "arborescence")

L'arborescence suit la logique *produce/consume*, avec 4 dossiers:  

- Un dossier */producer* contenant le *producer.py* : c'est lui qui enverra les messages dans le topic.
[Voir README.md du producer](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/src/master/producer/README.md)

- Un dossier */consumer* contenant deux consumer:
    -  un *consumer.py* Celui-ci se contente d'envoyer les messages par paquet dans Hive après les avoir récupéré dans le topic correspondant. **ATTENTION** Ces messages seront lus en streaming. Ainsi si ce consumer n'est pas lancé ou ne fonctionne pas au moment de la diffusion des messages par le producer, il ne pourra pas les récupérer.
    -  un *consumer_from_position.py* qui récupère comme le fichier précédant les messages depuis un topic. Cependant, celui-ci se base sur un système permettant de récupérer les messages depuis le dernier *offset* du dernier paquet envoyé. Ainsi, si une erreur survient et que ce *consumer* est arrêté, il récupèrera quand même les messages envoyés par le producer même s'il n'était pas en cours d'exécution.
[Voir README.md des consumers](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/src/master/consumer/README.md)

- Un dossier */params*. Il contient deux fichiers:
    - le fichier *params.json*, qui stocke les différents paramètres qui sont nécessaires à la connexion à la base données.
    - le fichier *config.json*, contenant les informations (clefs et tokens) afin de pouvoir se connecter à l'API Twitter.
[Voir README.md des paramètres](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/src/master/params/README.md)

- Enfin, le dossier */logger_kafka* contient 3 fichiers, rassemblant les logs du producer ainsi que des deux consumers.


## LET'S GO!

### Après avoir convenablement paramétré le fichier *params.json* ainsi que le *config.json*, nous pouvons commencer.

1. Pour ce faire, il faut se rendre dans le dossier */consumer* et lancer celui qui correspondra le mieux:
``` bash
python consumer_from_position.py
```

2. On lance ensuite le *producer.py* se trouvant dans le dossier du même nom. Il prend 1 argument, à savoir le # de la tendance que nous souhaitons récolter:
``` bash
python producer.py bigdata
```
