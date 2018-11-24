#!/bin/bash
echo "Installing 'spc' command"
cp spc /usr/bin/
chmod 777 /usr/bin/spc
echo "Command Installed"
#help2man -o spc.txt spc
#cp spc.txt spc.2
#gzip spc.2
echo "Installing man page"
cp spc.1.gz /usr/share/man/man1/
echo "Man page Installed"
#sudo echo "Rohan"
echo "Refer to 'man spc' for any help"
