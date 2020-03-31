# NotACrypter
NotACrypter est un logiciel réalisé avec Python 3.8.1 par Lucas et Alexandre, ce logiciel a pour but de permettre diverses action de cryptographie telles que :

- Le hashage d'un message / fichier
- L'utilisation d'un sel pour le processus de hashage
- La génération de clés AES
- Le chiffrement de texte / fichier via clé AES
- Le déchiffrement de texte / fichier via clé AES

## Installation
Pour executer ce script, nous vous recommandons la version 3.8.1 de Python pour évitez tout problème.

Vous devrez ensuite installer la librairie cryptography via cette commande :
`python -m pip install cryptography`

Vous pourrez enfin executer le script en utilisant la commande :
`python .\notACrypter.py`

## Utilisation
Pour ce qui est des répertoires, vous avez un dossier `output` qui a son tour contient 2 dossiers (`encrypted` et `decrypted`)
Tous les fichiers que vous chiffrerez via le logiciel finiront dans le dossier `encrypted` et tout les fichiers que vous déchiffrerez via le logiciel atterriront dans le dossier `decrypted`
