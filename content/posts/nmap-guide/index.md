---
layout: post
title: Nmap Guide
categories: markdown
summary: "Nmap, abréviation de *Network Mapper*, est un outil polyvalent et puissant qui peux se montrer utile autant pour un particulier q'un professionnel de la sécurité informatique cherchant à analyser, explorer et sécuriser..."
tags: [Nmap, Network Analysis]
date: 2023-09-23
---



Dans le domaine du pentesting et des CTF (Capture The Flag), la phase d'énumération est une étape cruciale. C'est là que l'outil Nmap entre en jeu. Nmap, abréviation de ``Network Mapper``, est un outil polyvalent et puissant qui peux se montrer utile autant pour un particulier q'un professionnel de la sécurité informatique cherchant à analyser, explorer et sécuriser un réseau.

Que ce soit pour auditer la sécurité de notre propre réseau, découvrir les dispositifs connectés ou évaluer la sécurité d'un réseau distant, Nmap est l'outil de prédilection. Grâce à ses fonctionnalités avancées, il permet de cartographier les hôtes du réseau, d'identifier les ports ouverts, les services en cours d'exécution, et bien plus encore.

Dans ce guide, nous explorerons de manière non-exhaustive mais autant que possible les différentes options d'analyse qu'offre Nmap et leurs utilités.

![banner](cover.png)
### I- Analyse du Réseau

Avant de plonger dans les techniques avancées d'analyse de ports offertes par Nmap, il est important de comprendre le fonctionnement général de cet outil et à quoi ressemble une commande standard de Nmap, ainsi que ses options par défaut.

- Fonctionnement Général de Nmap

L'outil ``Nmap`` fonctionne en envoyant des paquets réseau à la cible et se sert de l'analyse des réponses pour déterminer entre autres quels ports sont ouverts, quels services sont en cours d'exécution sur ces ports, et quelles sont les adresses IP des hôtes actifs sur le réseau. Il utilise différentes techniques de scan (que nous verront dans la section suivante) pour accomplir ces tâches. Chacune de ces techniques ayant leurs propres utilités, avantages et inconvénients en termes de discrétion, vitesse et détection.

- Commande Standard de Nmap

Une commande standard de Nmap suit généralement la structure suivante :

``nmap [options] [cibles]``

> Les "options" permettent de spécifier les paramètres du scan, tels que les techniques de scan à utiliser, les types de ports à scanner, etc. Les "cibles" sont les adresses IP ou les plages d'adresses à scanner.

### II- Techniques de Scans

   - L'option ``-sS`` exécute un ``scan SYN``, qui ne complète pas la connexion TCP et ne laisse aucune trace, ce qui le rend idéal pour une utilisation discrète, mais nécessite souvent des privilèges.

- Avec ``-sT``, Nmap effectue un scan connecté, complétant la connexion TCP. Bien que cette méthode laisse une trace, elle peut être utilisée en toute sécurité sans privilèges.

- Le ``scan UDP``, activé par ``-sU``, est plus lent car il teste les ports UDP, notamment ceux utilisés par des services comme ``DNS``(port 53), ``SNMP``(port 161/163) et ``DHCP`` (port 67/68).

- ``-sY`` utilise le protocole ``SCTP``, qui échoue à établir la connexion, évitant ainsi les journaux. Cela fonctionne de manière similaire à ``-PY.

- Les ``scans Null`` (-sN), ``Fin`` (-sF) et ``Xmas`` (-sX) envoient des paquets avec des flags TCP spécifiques pour pénétrer certains pare-feu et extraire des informations.

- Le ``scan Maimon`` (-sM) envoie des flags FIN et ACK, principalement pour BSD, mais actuellement, il rapportera tous les ports comme fermés.

- Les ``scans ACK`` (-sA) et ``Window`` (-sW) sont utilisés pour détecter les pare-feu en examinant la manière dont ils répondent aux paquets.

- Le ``scan Idle`` (-sI) est utilisé lorsque nous savons qu'un pare-feu ne filtre pas certaines IP, permettant une reconnaissance plus discrète.

- L'option ``--badsum`` envoie une somme de contrôle incorrecte, ce qui peut provoquer des réponses inattendues des pare-feu.

- Le scan ``SCTP Weird`` (-sZ) peut passer à travers des pare-feu, mais ne distingue pas entre les ports filtrés et ouverts.

- Le ``scan de protocole IP`` (-sO) envoie des en-têtes mal formés pour analyser les protocoles IP.

- L'option ``-b <server>`` est utilisée pour scanner un hôte depuis un autre via FTP, mais est peu utile en pratique dans la plupart des cas.

#### Découverte d'Équipement

Lorsque Nmap lance sa phase de découverte, il utilise par défaut une combinaison de techniques pour identifier les équipements actifs sur le réseau, comprenant : -PA80 -PS443 -PE -PP. Ces options sont des spécifications de types de sondes utilisées par défaut par Nmap lors de la phase de découverte des équipements sur le réseau.

> ``PA80`` : Cette option signifie que Nmap envoie des paquets ``TCP SYN`` vers le ``port 80`` (HTTP) des hôtes pour tenter d'initier une connexion. Le port 80 est souvent utilisé pour les ``serveurs web``.

> ``PS443`` : Cela indique à Nmap d'envoyer des paquets ``TCP SYN`` vers le ``port 443`` (HTTPS) pour tester la connectivité. Le port 443 est généralement utilisé pour les connexions sécurisées ``HTTPS``.

> ``PE`` : Cette option signifie que Nmap envoie des paquets ``ICMP Echo Request`` pour tester la connectivité avec les hôtes. Il s'agit d'une méthode non intrusive de vérification de la disponibilité des hôtes sur le réseau.

> ``PP`` : Cela indique à Nmap d'envoyer des paquets ``ICMP Timestamp Request`` pour vérifier la connectivité avec les hôtes. Il s'agit également d'une méthode non intrusive de vérification de la disponibilité des hôtes.

Ainsi, en utilisant une combinaison de ces sondes, Nmap peut identifier les équipements actifs sur le réseau et établir une base de données sur laquelle il pourra ensuite effectuer des scans plus approfondis des ports et des services

- ``sL`` : Ce scan non intrusif permet de lister les cibles en effectuant des ``requêtes DNS`` pour la ``résolution des noms``. C'est une approche discrète pour obtenir une liste d'équipements actifs.

- ``Pn`` : En désactivant le ping, cet option indique à Nmap de ne pas effectuer de vérification de la disponibilité des hôtes via le ping. Utile si vous êtes sûr que toutes les cibles sont actives.

- ``sn`` : Ce scan ne fait pas de scan de ports après la phase de reconnaissance, ce qui le rend relativement discret et adapté à une découverte rapide du réseau.

- ``PR`` : En utilisant le ``ping ARP``, cette option est souvent utilisée par défaut lors de l'analyse des ordinateurs dans votre propre réseau local.

- ``-PM`` : Effectue un ping ``ICMP address mask`` pour vérifier si la cible est active.

- ``PS <ports>`` : Envoie des paquets ``SYN`` pour tester la connectivité des ports. Les réponses indiquent si le port est ouvert, fermé ou injoignable.

- ``PA <ports>`` : Similaire à l'option précédente, mais en utilisant des paquets ``ACK``. La combinaison des deux peut donner de meilleurs résultats.

- ``PU <ports>`` : Envoie des sondes à des ports censés être fermés, ce qui est utile pour tester les pare-feu.

- ``PY <ports>`` : Envoie des sondes ``SCTP INIT``, généralement au port 80(HTTP) par défaut, pour détecter l'état ouvert/fermé/inactif des ports.

-``PO <protocols>`` : Indique les protocoles dans les en-têtes, par défaut ``ICMP (1)``, ``IGMP (2)`` et ``Encap IP (4)``.


**Autres Options :**

- ``-n`` : Désactive la résolution DNS, ce qui peut accélérer le scan en évitant la résolution de noms d'hôtes.

- ``-R`` : Force la résolution DNS pour toutes les cibles, garantissant ainsi l'affichage des noms d'hôtes dans les résultats du scan.


#### Options de Port

- ``-p «ports»``: Permet de spécifier les ports à scanner. Utilisez cette option suivie de la liste des ports que vous souhaitez scanner. Par exemple, pour scanner tous les ports, vous pouvez utiliser ``-p-`` ou ``-p all``.

- ``-F``: Ce paramètre permet de réaliser un scan rapide en ne vérifiant que les 100 ports les plus couramment utilisés.

- ``--top-ports «nombre»``: Cette option vous permet de spécifier le nombre de ports les plus courants à scanner, de 1 à 65335.

- ``-r``: Ce paramètre indique à Nmap de scanner les ports dans un ordre aléatoire, ce qui peut aider à éviter la détection par les systèmes de sécurité.

- ``--port-ratio <ratio>`` : Cette option permet d'analyser les ports les plus courants en spécifiant un ratio entre 0 et 1. Cela permet de focaliser l'analyse sur les ports les plus susceptibles d'être ouverts.


#### Scan de Version (-sV)

- ``-sV``: L'option de scan de version permet à Nmap d'identifier les versions des services qui tournent sur les ports ouverts. Vous pouvez régler l'intensité de ce scan de 0 à 9, avec 7 comme valeur par défaut.

- ``--version-intensity «nombre»``: Cette option vous permet de régler l'intensité du scan de version. Une intensité plus basse lancera uniquement les sondes les plus probables, ce qui réduit le temps de scan, notamment pour les scans UDP.


#### Détection d'OS (-O)

- ``-O``: L'option -O permet à Nmap de tenter de détecter le système d'exploitation des hôtes analysés en analysant diverses caractéristiques des paquets réseau.

- ``--osscan-limit``: Si cette option est activée, Nmap n'essaiera pas de prédire l'OS si moins de 2 ports (un ouvert, un fermé) sont détectés, ce qui économise du temps de scan.

- ``--osscan-guess``: Cette option améliore la détection d'OS en cas d'incertitude, en effectuant une analyse plus poussée des réponses réseau.


#### Scripts

- ``--script «nom_fichier» | «catégorie» | «répertoire» | «expression» [,...]``: Cette option permet de spécifier les scripts à exécuter pendant le scan. Vous pouvez spécifier un nom de fichier, une catégorie, un répertoire ou une expression. Utilisez ``-sC`` ou ``--script=default`` pour exécuter les scripts par défaut.

    - ``Auth``: Exécute tous les scripts disponibles pour l'authentification.
    - ``Default``: Exécute les scripts par défaut de la catégorie.
    - ``Discovery``: Récupère des informations sur la cible.
    - ``External``: Utilise des ressources externes.
    - ``Intrusive``: Utilise des scripts considérés comme intrusifs.
    - ``Malware``: Recherche des connexions ouvertes par des codes malveillants.
    - ``Safe``: Exécute des scripts non intrusifs.
    - ``Vuln``: Découvre les vulnérabilités connues.
    - ``All``: Exécute tous les scripts NSE disponibles.

- Pour rechercher des scripts:

    - `nmap --script-help="http-*"`: Scripts commençant par "http-".
    - `nmap --script-help="not intrusive"`: Tous sauf les intrusifs.
    - `nmap --script-help="default or safe"`: Ceux qui sont dans l'un ou l'autre ou les deux.
    - `nmap --script-help="default and safe"`: Ceux qui sont dans les deux.
    - `nmap --script-help="(default or safe or intrusive) and not http-*"`.

- ``--script-args «n1»=«v1»,«n2»={_«n3»=«v3»},«n4»={_«v4»_,_«v5»}``: Permet de spécifier des arguments pour les scripts. Vous pouvez spécifier des valeurs pour des arguments individuels ou des ensembles d'arguments.

- ``--script-args-file «nom_fichier»``: Cette option lit les arguments depuis un fichier spécifié, ce qui peut être utile pour des configurations complexes.

- ``--script-help «nom_fichier» | «catégorie» | «répertoire» | «expression» | all[,...]``: Cette option fournit de l'aide sur les scripts. Vous pouvez spécifier un nom de fichier, une catégorie, un répertoire, une expression ou simplement ``all`` pour obtenir une aide complète.

- ``--script-trace``: Cette option fournit des informations détaillées sur l'exécution des scripts, ce qui peut être utile pour le débogage.

- ``--script-updatedb``: Cette option met à jour la base de données des scripts, ce qui peut être nécessaire pour intégrer de nouveaux scripts ou des mises à jour.


#### Contrôle du Temps

- Nmap peut ajuster le temps en secondes, minutes, ou millisecondes : Vous pouvez définir le temps en utilisant `--host-timeout arguments 900000ms`, `900`, `900s`, et `15m` qui effectueront tous la même tâche.
  
- `--min-hostgroup «numhosts»; --max-hostgroup «numhosts»`: Ces options ajustent la taille des groupes d'analyse en parallèle.

- `--min-parallelism «numprobes»; --max-parallelism «numprobes»`: Ces options contrôlent le nombre de scanneurs en parallèle.

- `--min-rtt-timeout «time», --max-rtt-timeout «time», --initial-rtt-timeout «time»`: Ces options modifient les délais de temps pour les connexions.

- `--max-retries «numtries»`: Cette option modifie le nombre de tentatives avant d'abandonner.

- `--host-timeout «time»`: Cette option modifie le temps de scan par hôte.

- `--scan-delay «time»; --max-scan-delay «time»`: Ces options ajustent le délai entre chaque test.

- `--min-rate «number»; --max-rate «number»`: Ces options modifient le nombre de paquets envoyés par seconde.

- `--defeat-rst-ratelimit`: Cette option permet d'accélérer le scan en ignorant les limites de réponse RST.


#### Contrôle de l'Aggressivité 

- `-T paranoid|sneaky|polite|normal|aggressive|insane`: Cette option ajuste l'agressivité du scan.
    - `-T0` (paranoid): Effectue un seul test à la fois, en attendant 5 minutes entre chaque test.
    - `-T1`(sneaky) et `-T2`(polite): Effectue les tests de manière similaire, mais en attendant respectivement 15 secondes et 0,4 secondes entre chaque test.
    - `-T3`(normal): C'est l'agressivité par défaut, incluant le parallélisme (équilibrage efficace de la vitesse du scan tout en maintenant une utilisation raisonnable des ressources).
    - `-T4`(agressive): tilise des paramètres prédéfinis pour un scan relativement rapide tout en évitant une utilisation excessive des ressources réseau. Il s'agit d'un bon compromis entre vitesse et prudence.
    - `-T5`(insane): Est considéré comme le niveau le plus agressif, utilisant toutes les ressources disponibles pour effectuer un scan aussi rapide que possible. Il s'agit du niveau le plus rapide, mais aussi du plus intrusif et risqué.


#### Firewall/IDS


- ``-f``: Cette option fragmente les paquets. Par défaut, Nmap fragmente les paquets en morceaux de ``8 octets`` après l'en-tête. Pour spécifier une taille de fragment différente, vous pouvez utiliser ``..mtu`` (dans ce cas, n'utilisez pas -f). Assurez-vous que le décalage est un ``multiple de 8``. Il est à noter que les scanners de version et les scripts ne prennent pas en charge la fragmentation.
  
- Masquage d'Adresse (-D)
	- ``-D decoy1,decoy2,ME``: Nmap envoie des scanners avec d'autres adresses IP comme origine pour vous cacher. Si vous ajoutez ME à la liste, Nmap vous positionnera là; il est préférable de mettre 5 ou 6 adresses avant la vôtre pour vous masquer complètement. Vous pouvez générer des adresses IP aléatoires avec RND:«nombre» pour générer «nombre» d'adresses IP aléatoires. Celles-ci ne fonctionnent pas avec la détection de versions sans connexion TCP. Si vous êtes dans un réseau, il est préférable d'utiliser des adresses IP qui sont actives, sinon il sera très facile de savoir que vous êtes la seule active.
  
- Pour utiliser des adresses IP aléatoires : `nmap -D RND:10 Ip_cible`

#### Spécification de l'Adresse Source (-S)

- ``-S IP``: Cette option permet de spécifier l'adresse IP source du paquet. Utile lorsque Nmap ne détecte pas automatiquement votre adresse IP ou pour faire croire qu'un autre hôte effectue le scan.

#### Sélection de l'Interface Réseau (-e)

- ``-e «interface»``: Cette option permet de choisir l'interface réseau à utiliser pour le scan.

> Notons que certains admin réseaux trouvent plus pratique de laisser de nombreux ports ouverts plutôt que de chercher des solutions alternatives. Ces ports, tels que les ports DNS ou FTP, peuvent présenter des vulnérabilités. Pour explorer ces failles potentielles, Nmap propose les options --source-port «numéro de port» et -g «numéro de port» (équivalents).


- ``--data`` _``«chaîne hexadécimale»``_: Cette option permet d'envoyer des données sous forme de texte en utilisant le format hexadécimal.

- ``--data-string`` _``«chaîne»``_: Cette option permet d'envoyer des données sous forme de texte normal.

- ``--data-length`` _``«nombre»``_: Cette option spécifie la longueur des données à envoyer. Nmap envoie uniquement les en-têtes et ajoute un nombre spécifié d'octets supplémentaires de manière aléatoire.
    

- ``--ip-options``: Utilisez cette option pour configurer complètement le paquet IP.

- ``--packet-trace``: Utilisez cette option si vous souhaitez voir les options dans les paquets envoyés et reçus.

- ``--ttl`` _``«valeur»``_: Cette option permet de spécifier la valeur TTL (Time to Live) pour les paquets.

- ``--randomize-hosts``: Cette option rend l'attaque moins évidente en randomisant l'ordre des cibles.

- ``--spoof-mac`` _``«adresse MAC, préfixe ou nom de fournisseur»``_: Utilisez cette option pour changer l'adresse MAC utilisée lors du scan. Vous pouvez spécifier une adresse MAC, un préfixe ou le nom d'un fournisseur.

- ``--proxies`` _``«liste d'URL de proxy séparées par des virgules»``_: Utilisez cette option pour utiliser des proxys. Notez que parfois, un proxy ne maintient pas autant de connexions ouvertes que Nmap le souhaite, donc vous devrez peut-être modifier le parallélisme avec `--max-parallelism`.

- ``-sP``: Utilisez cette option pour découvrir les hôtes dans le réseau avec ARP.


#### Sorties

- ``-oN file`` : Produit une sortie normale dans le fichier spécifié.
    
- ``-oX file`` : Produit une sortie XML dans le fichier spécifié.
    
- ``-oS file`` : Produit une sortie conçue pour les script kiddies dans le fichier spécifié.
    
- ``-oG file`` : Produit une sortie au format greppable dans le fichier spécifié.
    
- ``-oA file`` : Produit toutes les sorties sauf -oS dans le fichier spécifié.
    
- ``-v level`` : Définit le niveau de verbosité.
    
- ``-d level`` : Définit le niveau de débogage.
    
- ``--reason`` : Affiche la raison de l'état de l'hôte.
    
- ``--stats-every time`` : Affiche les statistiques à intervalles réguliers.
    
- ``--packet-trace`` : Affiche les paquets envoyés.
    
- ``--open`` : Affiche les ports ouverts et leur état.
    
- ``--resume file`` : Permet de reprendre une analyse à partir d'un fichier de reprise.

### Divers

- ``-6`` : Active la prise en charge d'IPv6.
    
- ``-A`` : Équivalent à -O -sV -sC --traceroute.

#### Exécution

Pendant l'exécution de Nmap, vous pouvez modifier les options en cours de route :

- ``v / V`` : Augmente / diminue le niveau de verbosité.
    
- ``d / D`` : Augmente / diminue le niveau de débogage.
    
- ``p / P`` : Active / désactive la traçabilité des paquets.
    
- ``?`` : Affiche une aide interactive.
  
#### Vulnscan

Les scripts de Nmap Vulnscan examinent les versions des services obtenues dans une base de données hors ligne (téléchargée depuis d'autres sources très importantes) et renvoient les vulnérabilités potentielles.

Les bases de données utilisées sont :

1. Scipvuldb.csv - [http://www.scip.ch/en/?vuldb](http://www.scip.ch/en/?vuldb)
2. Cve.csv - [http://cve.mitre.org](http://cve.mitre.org/)
3. Osvdb.csv - [http://www.osvdb.org](http://www.osvdb.org/)
4. Securityfocus.csv - [http://www.securityfocus.com/bid/](http://www.securityfocus.com/bid/)
5. Securitytracker.csv - [http://www.securitytracker.com](http://www.securitytracker.com/)
6. Xforce.csv - [http://xforce.iss.net](http://xforce.iss.net/)
7. Exploitdb.csv - [http://www.exploit-db.com](http://www.exploit-db.com/)
8. Openvas.csv - [http://www.openvas.org](http://www.openvas.org/)

Il est également nécessaire de télécharger les paquets des bases de données et de les ajouter à /usr/share/nmap/scripts/vulscan/.

Utilisation :

- Pour tout utiliser :

```bash
sudo nmap -sV --script=vulscan <HOST>

```

- Pour utiliser une base de données spécifique :

```bash
sudo nmap -sV --script=vulscan --script-args vulscandb=cve.csv <HOST>
```

### Accélérer l'analyse des services de Nmap x16

Selon [cette publication](https://joshua.hu/nmap-speedup-service-scanning-16x), vous pouvez accélérer l'analyse des services Nmap en modifiant toutes les valeurs `totalwaitms` dans `/usr/share/nmap/nmap-service-probes` à ``300`` et `tcpwrappedms` à ``200``.

De plus, les sondes qui n'ont pas de `servicewaitms` spécifiquement défini utilisent une valeur par défaut de ``5000``. Par conséquent, nous pouvons soit ajouter des valeurs à chacune des sondes, soit compiler Nmap nous-mêmes et changer la valeur par défaut dans [service_scan.h](https://github.com/nmap/nmap/blob/master/service_scan.h#L79).

Si vous ne souhaitez pas du tout changer les valeurs `totalwaitms` et `tcpwrappedms` dans le fichier `/usr/share/nmap/nmap-service-probes`, vous pouvez modifier le [code d'analyse](https://github.com/nmap/nmap/blob/master/service_scan.cc#L1358) de manière à ce que ces valeurs dans le fichier `nmap-service-probes` soient complètement ignorées.



En conclusion, l'utilisation de Nmap offre une gamme très variée d'options pour l'analyse des réseaux, la détection des services et la détection d'éventuelles vulnérabilités. En explorant ses fonctionnalités et en ajustant certains paramètres, il est possible d'optimiser l'analyse et accélérer le processus de découverte et de sécurisation des réseaux informatiques. Que ce soit pour des besoins de sécurité, de dépannage réseau ou de gestion des actifs, Nmap reste un outil précieux et polyvalent pour les tâches de scanning réseau.