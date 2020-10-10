#!/bin/bash

ssh-add -D
echo 'Before:'
ssh-add -L
./inicerts.py -i
echo 'After:'
ssh-add -L
