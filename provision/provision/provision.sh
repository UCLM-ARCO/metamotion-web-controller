#!/bin/sh

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install ansible openssh-server sshpass
dpkg -i metamotion_0.20200531-1_all.deb

sudo service ssh restart

#cp ansible/ansible.cfg ~/.ansible.cfg
sudo ansible-playbook -i localhost, -u pi -k playbook.yml

