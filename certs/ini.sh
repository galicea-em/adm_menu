#!/bin/bash

sudo apt install expect
echo "Użyj maila takiego jak ustawiasz w inicerts.py"
mkdir ~/.gnupg
chmod 700 ~/.gnupg
mkdir -p ~/.gnupg/private-keys-v1.d
chmod 700 ~/.gnupg/private-keys-v1.d
gpg --gen-key



echo -n "Ident. (ssh key):"
read key

echo -n "Password (ssh key):"
read -s Password

echo "... adding to store ...."

./inicerts.py -a $key -p "$Password"
