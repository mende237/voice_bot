#!/bin/bash

# on recupere le nom d'utilisateur d'asterixsk et le tien
read -p "votre nom d'utilisateur : " my_user;
read -p "le nom d'utilisateur d'asterisk : " asterisk_user;

#on cree le groupe voice_bot et l'utilisateur voice_bot
sudo useradd voice_bot

#on integre asterisk et soi meme dans le groupe voice_bot
sudo adduser $my_user voice_bot
sudo adduser $my_user voice_bot

#on change les acces a l'application
sudo chgrp voice_bot voice_bot
sudo chmod 775 voice_bot
sudo chmod 775 voice_bot/*

