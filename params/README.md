# FICHIERS DE PARAMETRAGE : CONNEXION KAFKA À HIVE
-------------------------

## Le fichier params.json:

**Ce fichier comporte différent paramètres que nous allons détailler ici:**

* topic : Nom du topic
* host_hive: Host sur lequel se trouve le client Hive. Dans notre cas, **localhost**
* user_hive: Nom d'utilisateur Hive
* password_hive: Mot de passe utilisateur Hive
* database_hive: Nom de la base de données (ici, default)

Ces données se trouvent dans *Services> Hive> Config> Advanced*

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/hive_params.png "Paramètres Hive")

* lenght_bloc : Nombre de messages constituant les blocs
* log_file: Différents chemins de destination des fichiers log
* table_hive : Nom de la table Hive
* cluster: Liste des adresses des différents brokers Kafka.
La liste des brokers se trouve dans *Services > Kafka> Kafka Brokers*. **ATTENTION: penser à enlever le port 2181 lors du remplissage de la liste!**

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/kafka-brokers.png "Brokers Kafka")


* server_port : Port des brokers kafka:

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/zookieper_port.png "Port Zookieper")

* zookieper_port: Port de zookieper

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/server_port.png "Port des Serveurs")


## Le fichier config.json:

**Ce fichier comporte les tokens et keys disponibles après avoir configué son compte Twitter développeur**
Toutes ces informations sont accessibles au moment de la création d'une application twitter:

![alt text](https://gitbox.affini-tech.net/Affini-Tech/Kafka-Hadoop/raw/master/images/twitter_dev_app.png "Application de dev Twitter")
