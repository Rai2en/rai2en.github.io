---
title: "HTB - Devvortex"
summary: "DevVortex est une machine Linux de niveau easy nécessitant un brute force DNS pour trouver un sous-domaine, suivi d'un brute force de répertoire qui mènera sur la découverte d'un dashboard admin **Joomla** obsolète..."
categories: ["Post","Blog",]
tags: ["HackTheBox","Writups"]
#externalUrl: ""
date: 2023-09-04
draft: false
---

[DevVortex](https://app.hackthebox.com/machines/devvortex) est une machine Linux de niveau easy nécessitant un brute force DNS pour trouver un sous-domaine, suivi d'un brute force de répertoire qui mènera sur la découverte d'un dashboard admin ``Joomla`` obsolète dont l'exploitation permettra de trouver des identifiants de connexion. Le dashboard administrateur servira ensuite à éditer des fichiers PHP pour obtenir un reverse shell. Les mêmes identifiants de connexion, seront ensuite utilisés pour avoir accès à un hash MySQL, qu'on déchiffrera avec John. La connexion via SSH révèlera ensuite l'utilisation d'une ancienne version ``apport-cli``, permettant l'exécution d'un shell root.