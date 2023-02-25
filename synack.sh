#!/usr/bin/bash

export ME=$(whoami | tr -d '\n')

sudo apt update
sudo apt install aptitude
sudo chown -R $ME: /opt/ 
sudo aptitude install zsh
sudo aptitude install sublime-text
sudo aptitude install crunch

git clone https://github.com/danielmiessler/SecLists.git /opt/SecLists
cd ~/Downloads/
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall && rm msfinstall
pwd
wget -q https://github.com/projectdiscovery/httpx/releases/download/v1.2.7/httpx_1.2.7_linux_amd64.zip
sleep 1

unzip httpx_1.2.7_linux_amd64.zip
rm ~/Downloads/httpx_1.2.7_linux_amd64.zip  &
rm ~/Downloads/LICENSE.md &
rm ~/Downloads/README.md &
mv ~/Downloads/httpx /opt/httpx

file /opt/httpx

wget -q https://github.com/projectdiscovery/nuclei/releases/download/v2.8.9/nuclei_2.8.9_linux_amd64.zip
sleep 1
unzip nuclei_2.8.9_linux_amd64.zip
rm ~/Downloads/nuclei_2.8.9_linux_amd64.zip &
mv ~/Downloads/nuclei /opt/nuclei
file /opt/nuclei

cd


sudo aptitude install -y libssl-dev libffi-dev python-dev-is-python3 build-essential
curl -sSL https://install.python-poetry.org | python3 -
curl -sSL https://install.python-poetry.org | python3 -
export PATH="~/.local/bin:$PATH"
git clone https://github.com/Porchetta-Industries/CrackMapExec /opt/CrackMapExec
cd /opt/CrackMapExec
sudo aptitude install python3-pip
~/.local/bin/poetry lock --no-update
~/.local/bin/poetry install
~/.local/bin/poetry run crackmapexec

alias crackmapexec='cd /opt/CrackMapExec; ~/.local/bin/poetry run crackmapexec'

cd ~/Downloads/
wget -q https://github.com/OJ/gobuster/releases/download/v3.5.0/gobuster_3.5.0_Linux_x86_64.tar.gz
tar xfvz gobuster_3.5.0_Linux_x86_64.tar.gz
rm gobuster_3.5.0_Linux_x86_64.tar.gz
rm LICENSE
rm README.md
mv gobuster /opt/
chmod +x /opt/gobuster
cd


cd ~/Downloads/
wget -q 'https://portswigger-cdn.net/burp/releases/download?product=pro&version=2023.1.2&type=Linux' -O burppro.sh
chmod +x burppro.sh
./burppro.sh


