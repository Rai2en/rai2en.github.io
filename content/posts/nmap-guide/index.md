---
layout: post
title: Nmap Guide
categories: markdown
summary: "Nmap, abréviation de *Network Mapper*, est un outil polyvalent et puissant qui peux se montrer utile autant pour un particulier q'un professionnel de la sécurité informatique cherchant à analyser, explorer et sécuriser..."
tags: [Nmap, Network Analysis]
date: 2023-09-23
---



Dans le cadre des tests d'intrusion (pentesting) et des défis CTF (Capture The Flag), la phase d'énumération constitue une étape essentielle. C'est ici que Nmap, un outil incontournable pour les professionnels de la sécurité informatique, entre en scène.

Nmap, abréviation de Network Mapper, est un utilitaire puissant et polyvalent, utilisé tant par les administrateurs réseau que par les experts en cybersécurité pour analyser, explorer et sécuriser les infrastructures réseau.

Que ce soit pour auditer la sécurité d'un réseau interne, identifier les dispositifs connectés ou évaluer la surface d'attaque d'un réseau distant, Nmap est un outil privilégié. Ses fonctionnalités avancées permettent de cartographier les hôtes d'un réseau, de détecter les ports ouverts, d'identifier les services actifs, et bien plus encore.

Dans ce guide, nous explorerons les différentes options d'analyse qu'offre Nmap, et nous examinerons leur pertinence dans divers contextes de sécurité.
![banner](cover.png)


### I- Analyse du Réseau

Avant d'explorer les techniques avancées de scan de ports offertes par Nmap, il est crucial de comprendre le fonctionnement général de cet outil et de se familiariser avec la syntaxe d'une commande standard ainsi que ses options par défaut.

- Fonctionnement Général de Nmap

L'outil ``Nmap`` fonctionne en envoyant des paquets réseau à la cible et se sert de l'analyse des réponses pour déterminer entre autres quels ports sont ouverts, quels services sont en cours d'exécution sur ces ports, et quelles sont les adresses IP des hôtes actifs sur le réseau. Il utilise différentes techniques de scan (que nous verront dans la section suivante) pour accomplir ces tâches. Chacune de ces techniques ayant leurs propres utilités, avantages et inconvénients en termes de discrétion, vitesse et détection.

- Commande Standard de Nmap

La structure d'une commande Nmap est généralement la suivante :

``nmap [options] [cibles]``

> Les ``options`` permettent de spécifier les paramètres du scan, tels que les techniques de scan à utiliser, les types de ports à scanner, etc. Les ``cibles`` désignent les adresses IP ou les plages d'adresses à scanner.

### II- Techniques de Scans

- Scan SYN (-sS): Ce type de scan envoie un paquet SYN sans finaliser la connexion TCP, ce qui le rend discret et difficile à détecter. Il est particulièrement utile pour les tests d'intrusion furtifs, mais nécessite souvent des privilèges administratifs.

- Scan Connecté (-sT): Contrairement au scan SYN, ce scan établit une connexion complète via TCP. Bien qu'il laisse une trace, il peut être exécuté sans privilèges élevés.

- Scan UDP (-sU): Ce scan teste les ports UDP, souvent utilisés par des services tels que DNS (port 53), SNMP (ports 161/163) et DHCP (ports 67/68). Il est généralement plus lent que le scan TCP en raison de la nature non connectée du protocole UDP.

- Scan SCTP INIT (-sY): Ce scan utilise le protocole SCTP, en envoyant un paquet INIT sans établir de connexion, similaire au SYN scan pour TCP. Il est utile pour éviter la journalisation des connexions.

- Scans Null (-sN), Fin (-sF), et Xmas (-sX): Ces scans envoient des paquets avec des combinaisons spécifiques de flags TCP (aucun, FIN, ou un ensemble de flags inhabituels) pour contourner certains pare-feu et extraire des informations sur les ports ouverts.

- Scan Maimon (-sM): Ce scan envoie des paquets avec les flags FIN et ACK, principalement destiné aux systèmes BSD. Cependant, il peut souvent rapporter tous les ports comme étant fermés dans les systèmes actuels.

- Scans ACK (-sA) et Window (-sW): Utilisés pour identifier la présence de pare-feu, ces scans se basent sur la manière dont les pare-feu réagissent aux paquets ACK et sur l'analyse des tailles de fenêtre TCP.

- Scan Idle (-sI): Ce scan permet une reconnaissance discrète en utilisant un hôte intermédiaire. Il est efficace lorsque certaines adresses IP ne sont pas filtrées par le pare-feu.

- Option --badsum: Envoie des paquets avec une somme de contrôle incorrecte pour provoquer des réponses inattendues des pare-feu, révélant potentiellement des informations sur leur configuration.

- Scan SCTP Weird (-sZ): Conçu pour contourner les pare-feu, ce scan est cependant limité par son incapacité à distinguer les ports filtrés des ports ouverts.

- Scan de Protocole IP (-sO): Ce scan envoie des en-têtes IP mal formés pour détecter les protocoles IP supportés par la cible.

- Scan par FTP Bounce (-b <serveur>): Permet de scanner une cible via un serveur FTP intermédiaire. Bien que peu utilisé dans la pratique, il reste une technique intéressante pour certains environnements spécifiques.

##### Découverte d'Équipement

Lors de la phase de découverte, Nmap utilise par défaut une combinaison de techniques pour identifier les équipements actifs sur le réseau. Ces techniques incluent les options suivantes : `-PA80`, `-PS443`, `-PE`, et `-PP`, qui spécifient les sondes utilisées par Nmap pour cette étape.

- **`PA80`** : Envoie des paquets `TCP SYN` vers le port 80 (HTTP) pour tenter d'établir une connexion. Le port 80 étant largement utilisé pour les serveurs web, cette option permet de vérifier la disponibilité des hôtes exécutant des services HTTP.
    
- **`PS443`** : Envoie des paquets `TCP SYN` vers le port 443 (HTTPS), utilisé pour les connexions sécurisées. Cela permet de tester la connectivité des hôtes via des services HTTPS.
    
- **`PE`** : Envoie des paquets `ICMP Echo Request` (requête de ping) pour vérifier la disponibilité des hôtes de manière non intrusive.
    
- **`PP`** : Envoie des paquets `ICMP Timestamp Request` pour tester la connectivité, offrant une autre méthode discrète pour identifier les hôtes actifs.
    

En combinant ces sondes, Nmap est capable d'identifier les équipements actifs sur le réseau, ce qui permet ensuite de procéder à des analyses plus approfondies des ports et des services.

##### Autres options de découverte

- **`sL`** : Ce scan non intrusif effectue des requêtes DNS pour la résolution des noms, ce qui permet de lister les cibles sans envoyer de paquets aux hôtes directement. Il s'agit d'une approche discrète pour recenser les équipements.
    
- **`Pn`** : Désactive le ping, instructant Nmap de ne pas vérifier la disponibilité des hôtes via ICMP. Utile lorsque vous savez que les cibles sont actives mais ne répondent pas aux requêtes de ping.
    
- **`sn`** : Réalise uniquement la découverte d'hôtes sans effectuer de scan de ports, ce qui le rend discret et efficace pour une cartographie rapide du réseau.
    
- **`PR`** : Utilise un `ping ARP` pour identifier les hôtes actifs sur un réseau local. Cette méthode est souvent utilisée par défaut sur les réseaux Ethernet, car elle est précise et rapide dans un environnement local.
    
- **`-PM`** : Effectue un ping `ICMP Address Mask Request` pour vérifier si l'hôte est actif.
    
- **`PS <ports>`** : Envoie des paquets `SYN` à des ports spécifiques pour tester leur connectivité. Les réponses permettent de déterminer si le port est ouvert, fermé, ou filtré.
    
- **`PA <ports>`** : Semblable à `PS`, mais en utilisant des paquets `ACK` pour tester les ports. Cette méthode peut être utilisée en complément pour obtenir des informations supplémentaires.
    
- **`PU <ports>`** : Envoie des sondes à des ports supposés fermés pour tester la réaction des pare-feu, une technique utile pour la détection des dispositifs de filtrage.
    
- **`PY <ports>`** : Envoie des sondes `SCTP INIT` pour déterminer l'état des ports (ouvert, fermé ou injoignable), généralement sur le port 80 par défaut.
    
- **`PO <protocols>`** : Spécifie les protocoles à inclure dans les en-têtes des paquets, par exemple `ICMP (1)`, `IGMP (2)`, ou `Encap IP (4)`.

- **`-n`** : Désactive la résolution DNS, ce qui permet d'accélérer le scan en évitant de résoudre les noms d'hôtes associés aux adresses IP.
    
- **`-R`** : Force la résolution DNS pour toutes les cibles, garantissant ainsi que les noms d'hôtes sont inclus dans les résultats du scan.
    

##### Options de Ports

- **`-p <ports>`** : Permet de spécifier les ports à scanner. Cette option est suivie de la liste des ports ou des plages que vous souhaitez analyser. Par exemple, pour scanner tous les ports, utilisez `-p-` ou `-p all`.
    
- **`-F`** : Effectue un scan rapide en ne vérifiant que les 100 ports les plus couramment utilisés, réduisant ainsi le temps d'analyse.
    
- **`--top-ports <nombre>`** : Spécifie le nombre de ports les plus courants à analyser, de 1 à 65 535, en fonction de leur fréquence d’utilisation sur les réseaux.
    
- **`-r`** : Force Nmap à scanner les ports dans un ordre séquentiel (et non aléatoire), ce qui peut être utile pour des tests de performance ou pour éviter certaines stratégies de détection de scan.
    
- **`--port-ratio <ratio>`** : Permet de focaliser l'analyse sur les ports les plus communément ouverts, en spécifiant un ratio entre 0 et 1. Cela peut optimiser les scans en se concentrant sur les ports les plus susceptibles d’être actifs.
    

##### Scan de Version (`-sV`)

- **`-sV`** : Cette option permet à Nmap d'identifier les versions des services actifs sur les ports ouverts. Elle envoie des sondes spécifiques pour obtenir des informations détaillées sur les services. Vous pouvez ajuster l'intensité du scan de version, sur une échelle de 0 à 9, avec une valeur par défaut de 7.
    
- **`--version-intensity <nombre>`** : Permet de contrôler l'intensité du scan de version. Une intensité plus faible lancera uniquement les sondes les plus probables, ce qui peut réduire la durée du scan, notamment dans le cadre de scans UDP.
    

##### Détection d'OS (`-O`)

- **`-O`** : Cette option active la détection du système d'exploitation (OS) en analysant les réponses des paquets réseau. Nmap tente d'identifier l'OS en fonction des caractéristiques des hôtes.
    
- **`--osscan-limit`** : Limite la détection d'OS si moins de deux ports (un ouvert et un fermé) sont détectés. Cela permet de réduire le temps de scan si les conditions d'analyse ne sont pas optimales.
    
- **`--osscan-guess`** : Améliore la précision de la détection en cas d'incertitude, en effectuant une analyse plus approfondie des réponses réseau. Cette option force Nmap à faire des prédictions même si les résultats sont partiels.


### III- Scripts


L'option `--script` de Nmap permet d'exécuter des scripts pendant les scans, augmentant ainsi la capacité de collecte d'informations. Ces scripts, appelés **Nmap Scripting Engine (NSE)**, peuvent être spécifiés de différentes manières : par nom de fichier, catégorie, répertoire ou à l'aide d'expressions régulières. Vous pouvez aussi exécuter des scripts prédéfinis via les options suivantes :

- **-sC** ou **--script=default** : Exécute les scripts par défaut, équivalents à `--script=default`, conçus pour fournir un bon aperçu des vulnérabilités sans être trop intrusifs.

##### Catégories de scripts disponibles

Les scripts NSE sont organisés en différentes catégories, chacune visant à analyser un aspect particulier de la cible :

- **Auth** : Scripts pour tester les mécanismes d'authentification.
- **Default** : Ensemble de scripts par défaut qui fournissent un bon point de départ pour des analyses initiales.
- **Discovery** : Scripts de découverte permettant d'obtenir des informations supplémentaires sur la cible.
- **External** : Scripts s'appuyant sur des ressources externes pour analyser la cible.
- **Intrusive** : Scripts pouvant provoquer des modifications ou un comportement inattendu sur la cible.
- **Malware** : Scripts qui détectent les indicateurs de compromission (IoC) associés à des logiciels malveillants.
- **Safe** : Scripts non intrusifs garantissant qu'aucune modification n'est apportée à la cible.
- **Vuln** : Scripts dédiés à la détection de vulnérabilités connues.
- **All** : Exécute l'ensemble des scripts NSE disponibles.

##### Recherche et filtrage des scripts

Pour affiner la sélection des scripts à utiliser, Nmap permet de rechercher des scripts spécifiques grâce à l'option `--script-help`. Celle-ci permet d'afficher des informations sur des scripts en fonction de leur nom, catégorie ou comportement. Exemples de recherches :

- `nmap --script-help="http-*"` : Affiche tous les scripts dont le nom commence par "http-".
- `nmap --script-help="not intrusive"` : Exclut les scripts intrusifs et liste les autres.
- `nmap --script-help="default or safe"` : Affiche les scripts appartenant aux catégories "default" ou "safe".
- `nmap --script-help="default and safe"` : Affiche les scripts qui sont à la fois dans les catégories "default" et "safe".
- `nmap --script-help="(default or safe or intrusive) and not http-*"` : Affiche les scripts des catégories "default", "safe" ou "intrusive" mais exclut ceux liés au protocole HTTP.

##### Utilisation des arguments de scripts

Certains scripts NSE peuvent recevoir des arguments pour personnaliser leur fonctionnement. Vous pouvez les spécifier via l'option `--script-args`, qui permet de passer des valeurs spécifiques à des paramètres de scripts :

- `nmap --script-args «n1»=«v1»,«n2»={_«n3»=«v3»},«n4»={_«v4»_,_«v5»}` : Permet de définir plusieurs ensembles d'arguments.

Si vous avez une configuration plus complexe ou des ensembles d'arguments récurrents, il est possible de les fournir à partir d'un fichier texte en utilisant `--script-args-file`, ce qui est particulièrement pratique pour les configurations automatisées.

##### Aide, débogage et mise à jour des scripts

- **--script-help «nom_fichier» | «catégorie» | «répertoire» | «expression» | all** : Cette option affiche de l'aide sur les scripts en fonction du fichier, de la catégorie, du répertoire, ou d'une expression régulière. Spécifier "all" affiche l'aide pour tous les scripts disponibles.
- **--script-trace** : Active le traçage détaillé de l'exécution des scripts, fournissant des informations précieuses pour le débogage ou la compréhension des interactions entre les scripts et la cible.
- **--script-updatedb** : Met à jour la base de données des scripts NSE installés, nécessaire lorsque vous ajoutez de nouveaux scripts ou effectuez des mises à jour sur les scripts existants.


### IV- Contrôle du Temps et de l'Aggressivité des Scans

Nmap propose plusieurs options pour ajuster le contrôle du temps et l'agressivité des scans, permettant ainsi de mieux gérer les ressources et d'adapter les performances en fonction des besoins spécifiques.

##### Contrôle du Temps

Nmap permet de configurer les délais et les performances des scans en utilisant des unités de temps variées (millisecondes, secondes, minutes) :

- **Temps de scan ajustable** : Vous pouvez définir le temps en utilisant des arguments tels que `--host-timeout`, qui accepte des formats variés : `900000ms`, `900`, `900s`, et `15m` effectuent tous la même tâche, soit un délai de 15 minutes.
    
- **Contrôle des groupes d'hôtes** :
    
    - `--min-hostgroup «numhosts»` et `--max-hostgroup «numhosts»` permettent de définir la taille des groupes d'hôtes analysés simultanément.
- **Contrôle du parallélisme** :
    
    - `--min-parallelism «numprobes»` et `--max-parallelism «numprobes»` contrôlent le nombre de sondes envoyées en parallèle.
- **Temps de réponse RTT (Round Trip Time)** :
    
    - `--min-rtt-timeout «time»`, `--max-rtt-timeout «time»`, et `--initial-rtt-timeout «time»` permettent d'ajuster les délais de réponse pour les connexions.
- **Nombre de tentatives** :
    
    - `--max-retries «numtries»` ajuste le nombre de tentatives avant d'abandonner une connexion.
- **Délai entre scans** :
    
    - `--scan-delay «time»` et `--max-scan-delay «time»` modifient le délai entre chaque test envoyé à un hôte.
- **Taux d'envoi de paquets** :
    
    - `--min-rate «number»` et `--max-rate «number»` ajustent le nombre de paquets envoyés par seconde, ce qui peut influencer la vitesse du scan.
- **Bypass des limites RST** :
    
    - `--defeat-rst-ratelimit` permet d'ignorer les limitations de réponse RST (Reset) sur certains réseaux, accélérant ainsi le scan.

##### Contrôle de l'Aggressivité

L'option `-T` dans Nmap ajuste le niveau d'agressivité du scan en modifiant divers paramètres comme les délais, le parallélisme, et la gestion des ressources. Les niveaux d'agressivité sont définis comme suit :

- **-T0 (paranoid)** : Effectue un test à la fois, en introduisant un délai de 5 minutes entre chaque test. Utilisé pour des scans extrêmement furtifs.
- **-T1 (sneaky)** : Ajoute un délai de 15 secondes entre chaque test.
- **-T2 (polite)** : Réduit le délai à 0,4 seconde, tout en restant discret.
- **-T3 (normal)** : Niveau par défaut, équilibrant vitesse et utilisation des ressources.
- **-T4 (aggressive)** : Optimise le scan pour une vitesse accrue tout en limitant l'impact réseau, adapté pour des scans relativement rapides sans trop de risques.
- **-T5 (insane)** : Utilise toutes les ressources disponibles pour un scan aussi rapide que possible. Ce niveau est le plus rapide mais aussi le plus intrusif, présentant des risques accrus de détection et de perturbation.


### V- Firewall/IDS: Options de Masquage et de Fragmentation dans Nmap

Nmap offre des fonctionnalités avancées pour contourner les systèmes de sécurité tels que les pare-feu et les systèmes de détection d'intrusion (IDS). Voici quelques-unes des principales options que vous pouvez utiliser pour améliorer la discrétion de vos scans.

###### Fragmentation des Paquets

- **Option `-f`** : Cette option permet de fragmenter les paquets envoyés lors du scan. Par défaut, Nmap divise les paquets en morceaux de **8 octets** après l'en-tête. Si vous souhaitez spécifier une taille de fragment différente, vous pouvez utiliser l'option `..mtu`, tout en veillant à ce que le décalage soit un **multiple de 8**. Il est important de noter que la fragmentation n'est pas prise en charge par les scanners de version et les scripts Nmap.

###### Masquage d'Adresse IP

- **Masquage d'Adresse avec `-D`** :
    
    - **Syntaxe** : `-D decoy1,decoy2,ME`
    - Cette option permet à Nmap d'envoyer des scans en utilisant d'autres adresses IP comme origine, ce qui aide à dissimuler votre adresse IP réelle. En ajoutant `ME` à la liste, vous indiquez à Nmap que vous souhaitez inclure votre adresse IP. Il est recommandé de positionner **5 à 6 adresses IP** fictives avant la vôtre pour obtenir un masquage optimal.
    - Vous pouvez également générer des adresses IP aléatoires à l'aide de l'option `RND:«nombre»`, où «nombre» représente le nombre d'adresses IP à générer. Il est à noter que ces adresses ne fonctionneront pas avec la détection de versions sans connexion TCP. Sur un réseau, il est conseillé d'utiliser des adresses IP qui sont actives ; sinon, il sera facile de déterminer que vous êtes l'unique hôte actif.
- **Utilisation d'adresses IP aléatoires** :
    
    - Par exemple, vous pouvez exécuter la commande suivante pour utiliser des adresses IP aléatoires lors d'un scan : 

``nmap -D RND:10 Ip_cible
``

##### Spécification de l'Adresse Source et Options Réseau dans Nmap


Nmap offre une variété d'options pour spécifier des adresses IP, sélectionner des interfaces réseau et configurer des paquets, ce qui permet d'adapter les scans à différents environnements et besoins.

##### Spécification de l'Adresse Source

- **Option `-S IP`** : Cette option permet de définir l'adresse IP source des paquets envoyés par Nmap. Elle est particulièrement utile lorsque Nmap ne parvient pas à détecter automatiquement votre adresse IP ou lorsque vous souhaitez faire croire qu'un autre hôte réalise le scan.

##### Sélection de l'Interface Réseau

- **Option `-e «interface»`** : Cette option permet de sélectionner l'interface réseau spécifique à utiliser pour le scan.

##### Pratiques de Sécurité

> Il est bon de noter que certains administrateurs réseau préfèrent laisser de nombreux ports ouverts, tels que les ports DNS ou FTP par exemple, plutôt que de rechercher des solutions alternatives. Cela peut exposer le réseau à des vulnérabilités. Pour explorer ces failles potentielles, Nmap propose des options telles que `--source-port «numéro de port»` et `-g «numéro de port»`, qui sont équivalentes et permettent d'exploiter ces ports.

### VI- Options Avancées pour les Paquets

- **`--data «chaîne hexadécimale»`** : Permet d'envoyer des données sous forme de texte en utilisant le format hexadécimal.
    
- **`--data-string «chaîne»`** : Permet d'envoyer des données sous forme de texte normal.
    
- **`--data-length «nombre»`** : Spécifie la longueur des données à envoyer. Nmap enverra uniquement les en-têtes et ajoutera un nombre spécifié d'octets supplémentaires de manière aléatoire.
    
- **`--ip-options`** : Utilisez cette option pour configurer entièrement les options du paquet IP.
    
- **`--packet-trace`** : Affiche les informations sur les paquets envoyés et reçus, ce qui peut être utile pour le débogage.
    
- **`--ttl «valeur»`** : Permet de spécifier la valeur TTL (Time to Live) des paquets envoyés.
    
- **`--randomize-hosts`** : Rend le scan moins évident en randomisant l'ordre des cibles, ce qui contribue à dissimuler les activités.
    
- **`--spoof-mac «adresse MAC, préfixe ou nom de fournisseur»`** : Change l'adresse MAC utilisée lors du scan, en spécifiant une adresse MAC, un préfixe ou le nom d'un fournisseur.
    
- **`--proxies «liste d'URL de proxy séparées par des virgules»`** : Utilisez cette option pour effectuer des scans à travers des proxys. Notez qu'un proxy peut ne pas maintenir autant de connexions ouvertes que Nmap le désire ; par conséquent, il peut être nécessaire de modifier le parallélisme avec l'option `--max-parallelism`.
    
- **`-sP`** : Utilisez cette option pour découvrir les hôtes dans un réseau à l'aide de l'ARP (Address Resolution Protocol).


### VII- Options de Sortie dans Nmap

Nmap propose plusieurs options pour personnaliser la sortie des résultats de scan. Ces options permettent de stocker les données dans différents formats, facilitant ainsi l'analyse ultérieure ou l'intégration dans d'autres outils.

##### Options de Sortie

- **`-oN file`** : Génère une sortie normale dans le fichier spécifié, offrant une vue lisible et structurée des résultats.
    
- **`-oX file`** : Produit une sortie au format XML dans le fichier spécifié, idéale pour les traitements automatisés et l'intégration avec d'autres outils d'analyse.
    
- **`-oS file`** : Crée une sortie conçue pour les utilisateurs peu expérimentés (souvent appelés "script kiddies"), facilitant la compréhension des résultats.
    
- **`-oG file`** : Produit une sortie au format greppable, permettant une recherche facile et rapide à l'aide d'outils de ligne de commande.
    
- **`-oA file`** : Génère toutes les sorties, sauf celle destinée aux script kiddies, dans le fichier spécifié. Cela inclut les formats normal, XML et greppable.
    

##### Options de Verbosité et de Débogage

- **`-v level`** : Définit le niveau de verbosité de la sortie, permettant d'ajuster la quantité d'informations affichées pendant le scan.
    
- **`-d level`** : Spécifie le niveau de débogage, fournissant des détails supplémentaires sur le fonctionnement interne de Nmap, ce qui peut être utile pour résoudre des problèmes.
    

##### Options d'Affichage d'État et de Statistiques

- **`--reason`** : Affiche la raison derrière l'état de chaque hôte, fournissant un contexte pour les résultats du scan.
    
- **`--stats-every time`** : Affiche les statistiques à intervalles réguliers pendant l'exécution du scan, permettant de suivre l'évolution du processus.
    
- **`--packet-trace`** : Montre les paquets envoyés et reçus, ce qui peut être utile pour le débogage ou pour mieux comprendre le comportement du scan.
    
- **`--open`** : Affiche uniquement les ports ouverts et leur état, facilitant ainsi la concentration sur les éléments importants des résultats.
    
- **`--resume file`** : Permet de reprendre une analyse à partir d'un fichier de reprise, ce qui est particulièrement utile pour les scans longs ou complexes.


Nmap propose un ensemble d'options supplémentaires qui améliorent la flexibilité et la fonctionnalité du scan. Ces options permettent d'adapter Nmap à des environnements variés et de répondre à des besoins spécifiques.

### VIII- Options Diverses

- **`-6`** : Active la prise en charge du protocole IPv6, permettant ainsi d'analyser des cibles utilisant ce protocole.
    
- **`-A`** : Exécute un ensemble de fonctionnalités avancées, équivalent à la combinaison de `-O` (détection du système d'exploitation), `-sV` (détection de version), `-sC` (exécution des scripts par défaut) et `--traceroute` (détermination du chemin vers l'hôte).
    

##### Modification des Options en Cours d'Exécution

Nmap permet d'ajuster certaines options pendant l'exécution, offrant une plus grande interactivité et réactivité :

- **`v / V`** : Augmente ou diminue le niveau de verbosité, permettant de contrôler la quantité d'informations affichées pendant le scan.
    
- **`d / D`** : Augmente ou diminue le niveau de débogage, fournissant plus ou moins de détails sur le processus interne de Nmap.
    
- **`p / P`** : Active ou désactive la traçabilité des paquets, ce qui peut être utile pour observer le comportement des paquets envoyés.
    
- **`?`** : Affiche une aide interactive, offrant un accès rapide aux commandes et options disponibles.

### IX- Nmap Vulnscan

Nmap inclut un ensemble de scripts Vulnscan qui analysent les versions des services détectées lors des scans. Ces scripts se réfèrent à une base de données hors ligne, contenant des informations cruciales sur les vulnérabilités potentielles associées aux versions de services identifiées.

##### Bases de Données Utilisées

Les scripts Vulnscan s'appuient sur plusieurs bases de données de vulnérabilités, que vous devez télécharger et ajouter au répertoire `/usr/share/nmap/scripts/vulscan/` pour les utiliser efficacement. Voici les bases de données recommandées :

1. Scipvuldb.csv - [http://www.scip.ch/en/?vuldb](http://www.scip.ch/en/?vuldb)
2. Cve.csv - [http://cve.mitre.org](http://cve.mitre.org/)
3. Osvdb.csv - [http://www.osvdb.org](http://www.osvdb.org/)
4. Securityfocus.csv - [http://www.securityfocus.com/bid/](http://www.securityfocus.com/bid/)
5. Securitytracker.csv - [http://www.securitytracker.com](http://www.securitytracker.com/)
6. Xforce.csv - [http://xforce.iss.net](http://xforce.iss.net/)
7. Exploitdb.csv - [http://www.exploit-db.com](http://www.exploit-db.com/)
8. Openvas.csv - [http://www.openvas.org](http://www.openvas.org/)

Il est également nécessaire de télécharger les paquets des bases de données et de les ajouter à /usr/share/nmap/scripts/vulscan/.

Pour tirer parti de Nmap Vulnscan, vous pouvez utiliser les commandes suivantes :

- **Pour effectuer une analyse complète avec Vulnscan :**

```bash
sudo nmap -sV --script=vulscan <HOST>

```

- Pour utiliser une base de données spécifique :

```bash
sudo nmap -sV --script=vulscan --script-args vulscandb=cve.csv <HOST>
```

Ces commandes permettent de détecter les vulnérabilités connues sur les services en cours d'exécution sur l'hôte ciblé, facilitant ainsi l'évaluation de la sécurité.


### X- Accélérer l'analyse des services de Nmap x16

Selon une [étude publiée](https://joshua.hu/nmap-speedup-service-scanning-16x), il est possible d'accélérer considérablement l'analyse des services avec Nmap en ajustant certains paramètres dans le fichier de configuration `/usr/share/nmap/nmap-service-probes`. Pour ce faire, modifiez toutes les occurrences de `totalwaitms` à `300` millisecondes et de `tcpwrappedms` à `200` millisecondes.

Par ailleurs, les sondes qui ne possèdent pas de valeur `servicewaitms` définie utilisent par défaut une valeur de `5000` millisecondes. Pour optimiser davantage les performances, vous pouvez soit attribuer des valeurs spécifiques à chacune des sondes, soit compiler Nmap vous-même en modifiant la valeur par défaut dans le fichier [service_scan.h](https://github.com/nmap/nmap/blob/master/service_scan.h#L79).

Si vous préférez ne pas modifier les valeurs `totalwaitms` et `tcpwrappedms` dans `/usr/share/nmap/nmap-service-probes`, une autre solution consiste à adapter le [code d'analyse](https://github.com/nmap/nmap/blob/master/service_scan.cc#L1358) de Nmap pour ignorer complètement ces valeurs lors de l'exécution.


En conclusion, Nmap est un outil essentiel pour les professionnels de la cybersécurité, et offre une vaste gamme de fonctionnalités pour l'analyse des réseaux, la détection des services et l'identification des vulnérabilités. En exploitant ses options flexibles et en ajustant les paramètres d'analyse, les utilisateurs peuvent non seulement accélérer le processus de découverte, mais également garantir une approche sécurisée. Que ce soit pour des audits de sécurité, des tests de pénétration ou le dépannage réseau, Nmap demeure un allié précieux dans la construction d'une infrastructure informatique robuste face à des menaces en constante évolution.