---
layout: post
title: "Secure Network Architecture Lab - Vagrant, Firewall, TLS and Hardening"
date: 2026-05-08
draft: false
summary: "Projet personnel de déploiement d'une architecture réseau sécurisée avec Vagrant: firewall, segmentation, serveur web HTTPS, base de données isolée, Fail2ban, tests d'attaque et validation défensive."
tags: [Network Security, Vagrant, Firewall, UFW, TLS, Fail2ban, Hardening, Infrastructure, Defensive Security]
categories: [post]
series: ["CyberLabs"]
showTableOfContents: true
tocPosition: right
---

## Introduction

Ce projet documente la conception, le déploiement et la sécurisation d'une petite architecture réseau d'entreprise en environnement virtualisé.

L'objectif est de construire une infrastructure reproductible avec Vagrant, puis de la durcir étape par étape:

- segmentation réseau
- firewall / routeur
- serveur web HTTPS
- base de données isolée
- chiffrement des données sensibles
- Fail2ban
- tests d'attaque contrôlés
- validation défensive

Le projet est orienté blue team et infrastructure security. Il montre comment passer d'une architecture fonctionnelle à une architecture défendable.

## Objectifs

Les objectifs du lab sont:

- automatiser le déploiement des machines virtuelles
- isoler les rôles réseau
- appliquer le principe du moindre privilège
- limiter l'exposition des services
- chiffrer les communications web
- protéger l'accès SSH
- valider les protections par des tests offensifs contrôlés

## Architecture cible

Le lab repose sur 4 machines virtuelles:

| VM | Rôle | Exemple IP |
|---|---|---|
| fw | pare-feu / routeur | 192.168.100.1 |
| web | serveur web | 192.168.100.20 |
| db | base de données | 192.168.100.30 |
| attacker | poste de test Kali | 192.168.100.10 |

L'architecture utilise deux zones:

- un accès NAT pour la sortie Internet contrôlée
- un réseau interne isolé pour les services applicatifs

## Pourquoi Vagrant

Vagrant permet de rendre le lab reproductible.

Avantages:

- déploiement rapide
- configuration déclarative
- environnement rejouable
- documentation sous forme d'infrastructure as code
- cohérence entre les VMs

Exemple conceptuel:

```ruby
Vagrant.configure("2") do |config|
  config.vm.define "fw" do |fw|
    fw.vm.box = "ubuntu/jammy64"
    fw.vm.network "private_network", ip: "192.168.100.1"
  end
end
```

## Segmentation réseau

Le firewall joue le rôle de passerelle entre les zones.

Objectifs:

- empêcher l'accès direct non contrôlé vers la base de données
- centraliser le routage
- filtrer les flux entrants
- autoriser uniquement les services nécessaires

Tests de connectivité:

```bash
ip a
ip route
ping 192.168.100.1
ping 192.168.100.20
ping 192.168.100.30
```

## Mise en place du routage

Sur la VM firewall, l'IP forwarding est activé:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Pour le rendre persistant:

```bash
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

Les VMs internes utilisent le firewall comme passerelle par défaut.

## Politique firewall

La stratégie appliquée est simple:

- tout bloquer par défaut
- autoriser uniquement ce qui est nécessaire
- journaliser les flux importants
- exposer le minimum de services

Exemple UFW:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Durcissement du serveur web

Le serveur web héberge une application simple exposée uniquement via HTTPS.

Installation:

```bash
sudo apt update
sudo apt install apache2 php -y
sudo systemctl enable apache2
sudo systemctl start apache2
```

Ports autorisés:

- SSH d'administration sur port non standard
- HTTPS

HTTP clair peut être redirigé ou désactivé selon le besoin.

## TLS avec certificat auto-signé

Génération d'une clé privée:

```bash
sudo openssl genrsa -out /etc/ssl/private/server.key 2048
```

Création d'un certificat:

```bash
sudo openssl req -new -x509 \
  -key /etc/ssl/private/server.key \
  -out /etc/ssl/certs/server.crt \
  -days 365
```

Activation SSL Apache:

```bash
sudo a2enmod ssl
sudo a2ensite default-ssl
sudo systemctl reload apache2
```

## Sécurisation de la base de données

La base de données ne doit jamais être exposée directement depuis Internet ou depuis le réseau attaquant.

Mesures appliquées:

- écoute limitée au réseau interne
- accès autorisé uniquement depuis le serveur web
- durcissement de l'installation
- comptes DB dédiés
- privilèges minimaux

Exemple:

```bash
sudo mysql_secure_installation
```

Règle réseau attendue:

```text
web -> db:3306 autorisé
autres hôtes -> db:3306 bloqué
```

## Chiffrement des données sensibles

Les données sensibles et sauvegardes peuvent être chiffrées avant stockage ou transfert.

Exemple avec GPG:

```bash
gpg --symmetric backup.sql
```

Objectifs:

- protéger les sauvegardes
- réduire l'impact d'une fuite de fichiers
- ajouter une couche de défense hors ligne

## Fail2ban

Fail2ban protège les services exposés contre les tentatives répétées.

Installation:

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

Exemple de contrôle:

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

## Validation par attaques contrôlées

## Scan réseau

Depuis la VM attaquante:

```bash
nmap -p- 192.168.100.10
nmap -p- 192.168.100.20
nmap -p- 192.168.100.30
```

Résultat attendu:

- le web expose uniquement les ports nécessaires
- la DB ne doit pas exposer MySQL directement
- le firewall limite l'accès administratif

## Test brute force SSH

Test contrôlé avec Hydra:

```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://192.168.100.1 -s 2222
```

Résultat attendu:

- aucun mot de passe valide
- bannissement automatique après plusieurs échecs
- logs Fail2ban visibles

## Test applicatif OWASP light

Un test rapide est réalisé avec `sqlmap` contre une route applicative de test.

```bash
sqlmap -u "https://192.168.100.20/app.php?id=1" --batch
```

Le but n'est pas d'exploiter l'application à tout prix, mais de vérifier que le lab permet aussi de tester des contrôles applicatifs.

## Test TLS

Contrôle de la configuration TLS:

```bash
nmap --script ssl-enum-ciphers -p 443 192.168.100.20
```

Points à vérifier:

- protocoles faibles désactivés
- ciphers faibles évités
- certificat présent
- redirection HTTP si nécessaire

## Documentation et signature

Le projet inclut aussi une logique d'intégrité documentaire avec OpenPGP.

Exemple:

```bash
gpg --full-generate-key
gpg --armor --detach-sign rapport.pdf
```

Objectif:

- garantir l'intégrité d'un livrable
- prouver qu'un document n'a pas été modifié
- introduire une approche cryptographique pratique

## Résultats obtenus

Les tests montrent que:

- la segmentation limite l'exposition de la base de données
- le firewall joue bien son rôle de point de contrôle
- HTTPS protège les échanges web
- Fail2ban réduit l'efficacité des attaques automatisées
- les scans révèlent uniquement les services attendus
- le lab est reproductible grâce à Vagrant

## Recommandations d'amélioration

Améliorations possibles:

- ajouter un reverse proxy
- utiliser Let's Encrypt dans un environnement public
- centraliser les logs avec Wazuh
- ajouter des dashboards SIEM
- automatiser la configuration avec Ansible
- intégrer des tests de conformité CIS
- ajouter des règles IDS/Suricata

## Ce que ce projet m'a apporté

Ce projet m'a permis de travailler:

- la conception réseau sécurisée
- le routage Linux
- le filtrage UFW
- la sécurisation Apache/TLS
- la protection SSH
- le cloisonnement d'une base de données
- la validation offensive d'une architecture défensive

## Conclusion

Ce lab montre qu'une architecture sécurisée ne repose pas sur un seul outil. Elle dépend d'un ensemble de décisions cohérentes: segmentation, filtrage, chiffrement, durcissement, supervision et tests réguliers.

C'est un projet que je peux enrichir progressivement avec une couche SIEM, une automatisation Ansible et des scénarios purple team plus avancés.
