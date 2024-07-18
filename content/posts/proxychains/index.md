---
layout: post
title: Proxychains Guide
categories: markdown
summary: ""
tags: [proxychains, Network]
date: 2023-09-23
---

Dans le domaine de la **cybersécurité** et des **tests de pénétration** (_pentesting_), l'anonymat en ligne est crucial. Les professionnels de la cybersécurité utilisent des outils comme **ProxyChains** pour masquer leur identité et contourner les restrictions géographiques. ProxyChains permet de rediriger le trafic à travers une série de serveurs proxy, rendant le traçage de l'origine du trafic extrêmement difficile. Cet article explore en profondeur l'utilisation de ProxyChains, de son installation sur des distributions populaires comme Kali et Ubuntu, à son utilisation sur diverses plateformes, y compris Windows. Nous examinerons également ses différentes applications, allant de la simple confidentialité à des scénarios plus complexes impliquant **SSH** et **Metasploit**.

## Table des matières

1. [Introduction à ProxyChains](#introduction-%C3%A0-proxychains)
2. [Applications de ProxyChains en Cybersécurité](#applications-de-proxychains-en-cybers%C3%A9curit%C3%A9)
3. [Comparaison entre ProxyChains et ProxyChains-ng](#comparaison-entre-proxychains-et-proxychains-ng)
4. [Installation de ProxyChains sur Kali](#installation-de-proxychains-sur-kali)
5. [Installation de ProxyChains sur Ubuntu](#installation-de-proxychains-sur-ubuntu)
6. [Utilisation de ProxyChains](#utilisation-de-proxychains)
7. [Intégration de ProxyChains avec Tor](#int%C3%A9gration-de-proxychains-avec-tor)
8. [Considérations pour l'utilisation de ProxyChains](#consid%C3%A9rations-pour-lutilisation-de-proxychains)
9. [Conclusion](#conclusion)

## Introduction à ProxyChains

Avant de plonger dans les détails de ProxyChains, il est important de comprendre le concept de proxy.

### Qu'est-ce qu'un Proxy ?

Un proxy est un serveur intermédiaire qui agit comme une passerelle entre un utilisateur et Internet. Par exemple, lorsque vous visitez un site web comme google.com, au lieu d'envoyer directement les paquets au serveur de Google, vous les envoyez d'abord au proxy, qui les transmet ensuite à Google. Ce mécanisme permet au serveur de destination de voir les informations du proxy plutôt que celles de l'utilisateur, offrant ainsi une confidentialité accrue.

### Qu'est-ce que ProxyChains ?

ProxyChains améliore ce concept en utilisant plusieurs serveurs proxy en chaîne. Le trafic part de votre machine, passe par plusieurs serveurs proxy avant d'atteindre la destination finale, rendant le traçage de votre adresse IP d'origine beaucoup plus difficile. ProxyChains supporte l'intégration avec **Tor**, **SOCKS** et les **proxys HTTP**, permettant une flexibilité et une sécurité accrues lors de la navigation sur Internet. Il peut également être configuré pour fonctionner avec des applications telles que **Nmap** et **SQLmap**.

## Applications de ProxyChains en Cybersécurité

ProxyChains est souvent utilisé dans le cadre de **tests de pénétration** ou de **red teaming** pour masquer l'origine du trafic et simuler des accès depuis différentes localisations ou adresses IP. En enchaînant plusieurs proxies, y compris des systèmes compromis, les red teamers peuvent mieux dissimuler leurs mouvements au sein d'un réseau, rendant leur détection plus difficile. De plus, il est possible de contourner des pare-feux restrictifs pour accéder à des ressources bloquées.

## Comparaison entre ProxyChains et ProxyChains-ng

**ProxyChains-ng**, ou "next generation", est une version améliorée du projet ProxyChains. Il propose des fonctionnalités avancées et une meilleure compatibilité. ProxyChains-ng est un programme UNIX qui intercepte les fonctions libc liées au réseau dans des programmes liés dynamiquement via une DLL préchargée. Il redirige les connexions via des proxies SOCKS4a/5 ou HTTP et supporte uniquement le protocole TCP.

## Installation de ProxyChains sur Kali

ProxyChains-ng est préinstallé sur Kali. Pour vérifier son installation, entrez la commande:

```bash
proxychains4
````


## Installation de ProxyChains sur Ubuntu

ProxyChains-ng n'est pas installé par défaut sur Ubuntu, mais peut être installé en suivant ces étapes :

1. Mettez à jour vos dépôts 😀

```bash
sudo apt update -y
````

2. Installez ProxyChains-ng :

```bash
sudo apt install proxychains4
````

3. Vérifiez l'installation en entrant :

```bash
proxychains4
````


## Utilisation de ProxyChains

Pour utiliser ProxyChains, vous devez d'abord configurer le fichier de configuration de ProxyChains pour y ajouter vos proxies. Ouvrez le fichier de configuration avec un éditeur de texte :

```bash
sudo nano /etc/proxychains4.conf
```

Ajoutez vos proxies à la fin du fichier en utilisant le format `<protocole> <IP> <port>`. Vous pouvez également configurer la manière dont ProxyChains utilise la liste des proxies (chaînes dynamiques, strictes, round-robin, ou aléatoires).

## Intégration de ProxyChains avec Tor

**Tor** (The Onion Router) permet une communication anonyme sur Internet en faisant transiter le trafic à travers plusieurs serveurs opérés par des bénévoles à travers le monde.

### Utilisation de Tor et ProxyChains

1. Installation de Tor

```bash
sudo apt install tor
```

2. Démarrage du service Tor
   
 ```bash
sudo service tor start
```

Assurez-vous que le fichier de configuration de ProxyChains utilise le proxy SOCKS sur le port 9050 (port par défaut de Tor). Ensuite, lancez votre navigateur via ProxyChains :

```bash
proxychains4 firefox
```

## Considérations pour l'utilisation de ProxyChains

Pour maximiser l'anonymat avec ProxyChains, il est crucial de choisir des proxies fiables et anonymes situés dans différentes régions géographiques. Des listes de proxies gratuits sont disponibles sur des sites comme GitHub, mais il est recommandé de les tester régulièrement pour éviter les proxies défaillants. Des services payants comme **Webshare** offrent des proxies fiables et anonymes.

## Conclusion

ProxyChains est un outil puissant pour améliorer l'anonymat en ligne et contourner les restrictions géographiques. Que vous soyez un professionnel de la cybersécurité ou un utilisateur soucieux de sa confidentialité, ProxyChains offre une flexibilité et une sécurité accrues pour vos activités en ligne. Explorez ses différentes fonctionnalités pour voir comment il peut répondre à vos besoins.

## Foire Aux Questions

### ProxyChains est-il meilleur qu'un VPN ?

Chaque solution a ses avantages. Les **VPN** encryptent votre trafic via un tunnel, tandis que ProxyChains redirige simplement le trafic à travers plusieurs proxies. Les VPN offrent un niveau de sécurité et de confidentialité plus élevé, mais pas nécessairement l'anonymat, puisque le fournisseur de VPN connaît votre identité.

### ProxyChains est-il préinstallé sur Kali ?

Oui, Kali inclut ProxyChains par défaut. Vous pouvez le vérifier avec la commande `proxychains4`.

### Pourquoi les hackers utilisent-ils des serveurs proxy ?

Les hackers utilisent des serveurs proxy pour masquer leur adresse IP et leur localisation, rendant leur traçabilité difficile.

### Quelle est la différence entre Tor et ProxyChains ?

**Tor** crypte le trafic entre chaque relais de son réseau, tandis que ProxyChains ne fournit pas de cryptage, comptant sur les serveurs proxy pour sécuriser le trafic.

---