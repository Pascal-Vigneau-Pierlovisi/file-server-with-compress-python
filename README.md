# file-server-with-compress-python
Application de Gestion de Fichiers avec Algorithme de Huffman
Cette application web permet de gérer des fichiers en utilisant l'algorithme de compression de Huffman. L'algorithme de Huffman est utilisé pour compresser et décompresser les fichiers, permettant ainsi une gestion efficace des données.

Fonctionnalités :
- Compression de fichiers en utilisant l'algorithme de Huffman.
- Décompression de fichiers compressés en utilisant l'algorithme de Huffman.
- Interface web conviviale pour une utilisation facile.
  
Installation de l'environnement virtuel :
- Assurez vous que python3 est installé sur votre machine
- Clonez le projet github sur votre machine
- Vous aurez alors 2 dossiers importants, python-flask-client qui est le dossier de l'application web faite en Flask qui représente le client, puis python-file-server qui représente le serveur
- Dans le dossier python-flask-client vous devez initialiser un environnement virtuel à l'aide de la commande "python3 -m venv venv", vous devrez lancer l'environnement virtuel (voir la documentation de python) et installer toutes les librairies utilisées dans ce projet (Observez tous les fichiers et installer toutes les librairies à l'aide de l'utilitaire "pip")
- Le dossier python-compression-original représente les sources sur lesquelles je me suis appuyer pour développer l'application en format web 💻
- ⚠️ Faire attention à ce que dans la configuration du client Flask et du serveur, les ports des Sockets soient les mêmes.
