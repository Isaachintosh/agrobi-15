#!/usr/bin/env bash
zsh
cp ./.devcontainer/.zshrc ~/.zshrc
source ~/.zshrc
apt install git
git config --global user.name 'isaachintosh'
git config --global user.email 'isaac.tuning@gmail.com'
git config --global --add safe.directory /opt