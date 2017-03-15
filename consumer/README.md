# FICHIERS CONSUMER : CONNEXION KAFKA À HIVE
-------------------------

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/consumer_general.png "Vue Global des consumers")

## Le fichier consumer.py:

**Ce fichier est un consumer simple. Il lit les messages en directe, ce qui implique qu'il soit lancé lors de l'envoie par le producer de messages dans le topic**

### Quelques infos sur ce consumer:

* récupère les messages en direct (streaming)
* se base sur la fonction "seek_to_end()" de la librairie Kafka consumer
* ne permet pas de récupérer les messages depuis un offset bien précis
* dispose d'un fichier *consumer.out*, contenant toutes les infos et logs le concernant.


## Le fichier consumer_from_position.py:

**Ce fichier est un consumer. Il lit les messages depuis le dernier offset enregistré, ce qui permet d'ajouter un niveau de sécurité**


### Quelques infos sur ce consumer (supposons la taille des blocs définie à 30 messages):

* Au lancement, il définit le premier offset dans le fichier *offset.cfg*
* Si le consumer s'arrête pendant l'envoie de messages **avant** la constitution du premier bloc de 30 messages, au relancement du consumer, il se basera sur ce premier offset
* À chaque fin de création de bloc, il stock l'offset du dernier message de ce bloc dans le fichier *offset.cfg*
* Si par exemple, pendant l'envoie en flot continue du producer, le consumer s'arrête après avoir stocké seulement 15 messages, il pourra au relancement, se baser sur le dernier offset du bloc précédent afin de continuer à récupérer les messages depuis celui-ci.
* dispose d'un fichier *consumer_from_position.out*, contenant toutes les infos et logs le concernant.

#### Un schéma sera plus explicite:

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/schema_offset.png "Le fonctionnement du consumer_from_position")
