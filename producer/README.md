# FICHIERS PRODUCER : CONNEXION KAFKA À HIVE
-------------------------


## Le fichier producer.py:

**Ce fichier est un producer simple ayant pour but de récupérer des données (en l'occurence des tweets) pour les envoyer dans un topic Kafka.**

### Quelques infos sur ce producer:

* récupère les tweet en direct en fonction d'un #
* se base sur l'API twitter en python, afin de récupérer diverses informations: dans notre le cas,
  les messages seront constitué du nom de l'utilisateur ayant créé le tweet, de son message et du hashtag en question.
  ``` bash
  msg = '@%s: %s' %(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
  ```
* dispose d'un fichier *producer.out*, contenant toutes les infos et logs le concernant.
