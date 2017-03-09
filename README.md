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
- Un dossier */consumer* contenant deux consumer:
    -  un *consumer.py* Celui-ci se contente d'envoyer les messages par paquet dans Hive après les avoir récupéré dans le topic correspondant. **ATTENTION** Ces messages seront lus en streaming. Ainsi si ce consumer n'est pas lancé ou ne fonctionne pas au moment de la diffusion des messages par le producer, il ne pourra pas les récupérer.
    -  un *consumer_from_position.py* qui récupère comme le fichier précédant les messages depuis un topic. Cependant, celui-ci se base sur un système permettant de récupérer les messages depuis le dernier *offset* du dernier paquet envoyé. Ainsi, si une erreur survient et que ce *consumer* est arrêté, il récupèrera quand même les messages envoyés par le producer même s'il n'était pas en cours d'exécution. [Voir README.md du producer](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/src/master/consumer/README.md)


## SOME FACTS ABOUT KAFKA'S TOPICS

* A topic is a category or feed name to which records are published. Topics in Kafka are always multi-subscriber

  A topic can have zero, one, or many consumers that subscribe to the data written to it.

For each topic, the Kafka cluster maintains a partitioned log that looks like this:

![alt text](https://kafka.apache.org/images/log_anatomy.png "log in kafka")


-----




## PRODUCER

* Producers publish data to the topics of their choice.

* The producer is responsible for choosing which record to assign to which partition within the topic.

* If there is more than one partition, after 10 minutes off sending messages, the producer will automatically switch to the next partition.


----


## CONSUMER

* Consumers label themselves with a consumer group name, and each record published to a topic is delivered to one consumer instance within each subscribing consumer group:

  ![alt text](http://blog.xebia.fr/wp-content/uploads/2016/03/consumer-group-apache-kafka-xebia.png "Consumption schema")

  * If all the consumer instances have the same consumer group, then the records will effectively be load balanced over the consumer instances.*

  * If all the consumer instances have different consumer groups, then each record will be broadcast to all the consumer processes.*

  ![alt text](https://kafka.apache.org/images/consumer-groups.png "consumer's groups")


-----


## GUARANTEES

* Messages sent by a producer to a particular topic partition will be appended in the order they are sent. That is, if a record M1 is sent by the same producer as a record M2, and M1 is sent first, then M1 will have a lower offset than M2 and appear earlier in the log (queue).

* A consumer instance sees records in the order they are stored in the log.


-----


## USAGE && PROJECTS REALISED

******
### Requirements :
******

   Before starting a project you slould install some packages:

``` bash
sudo apt-get update
sudo apt-get install python-dev python-pip
sudo apt-get install openjdk-7-jre
```

   Then, install all the python packages:

``` bash
sudo pip install -r requirements.txt
```


Kafka can be used as a :

- Simple pubsub: [README.md of the project Pubsub](https://gitbox.affini-tech.net/Affini-Tech/Kafka/src/master/Projects/pubsub/README.md)

- PubSub with 3 servers (multi-broker): [README.md of the project pubsub-multi-broker](https://gitbox.affini-tech.net/Affini-Tech/Kafka/src/master/Projects/pubsub-multi-broker/README.md)

- PubSub with a Multi-broker and 2 consumers: [README.md of the project pubsub-multiple-consumer](https://gitbox.affini-tech.net/Affini-Tech/Kafka/src/master/Projects/pubsub-multiple-consumer/README.md)

- PubSub with a Multi-broker, multi-partitions and multi-consumers: [README.md of the project multi-broker-partition-consumer](https://gitbox.affini-tech.net/Affini-Tech/Kafka/src/master/Projects/multi-broker-partition-consumer/README.md)

- PubSub with a Mutli-broker, one-partition, fetching data from a specified timestamp: [README.md of the project multi-broker-partition-consumer-timestamp](https://gitbox.affini-tech.net/Affini-Tech/Kafka/src/master/Projects/multi-broker-partition-consumer-timestamp/README.md)

- PubSub with a Multi-broker, multi-partition, fetching data from a specified timestamp: [README.md of the project multi-broker-partition-timestamp](https://gitbox.affini-tech.net/Affini-Tech/Kafka/src/master/Projects/multi-broker-partition-timestamp/README.md)

- Kafka Streaming: [README.md of the project streaming](https://gitbox.affini-tech.net/Affini-Tech/Kafka/src/master/Projects/streaming/README.md)
