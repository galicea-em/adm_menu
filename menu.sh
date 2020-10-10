#!/bin/bash

KEY="cnz"
KEYPATH="$HOME/.ssh/$KEY"
CERT="$HOME/.ssh/$KEY.pub"
USER=jurek
INI=$1
PRIVATE_NET=10.0.0.0/8
PRIVATE_HOST=10.0.0.13
TUN=tun0
HEIGHT=25
WIDTH=40
CHOICE_HEIGHT=15
BACKTITLE="Wybór opcji"
TITLE="Serwery"
MENU="** EXAMPLE **"

OPTIONS=(0 "następna strona"
         1 "listuj pamięć"
         2 "ent"
         3 "poczta"
         4 "DEV"
         5 "doc1"
         )

if /sbin/ifconfig tun0 | grep -q "00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00"
then
   if ping -c 1 $PRIVATE_HOST &> /dev/null
   then
     echo "siec dostępna"
   else
     echo "ustawiam trasę z sieci zdalnej"
     sudo ip route add $PRIVATE_NET dev $TUN
   fi
#   read e
fi


CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear
case $CHOICE in
        0)
            ./menu2.sh $INI
            ;;
        1)
            ./certs.sh;./menu.sh
            ;;
        2)
            IP="10.0.0.111"
            ;;
        3)
            IP="10.0.0.112"
            ;;
        4)
            IP="10.0.0.113"
            ;;
        5)
            IP="10.0.0.114"
            ;;
        6)
            IP="10.0.0.115"
            ;;
        *) 
           exit 0
           ;;
esac

if [  "-i" = "$INI" ];
then
  if [ ! -f "$CERT" ];  then
    ssh-keygen -t rsa -b 2048  -f $KEY
    mv $KEY*  ~/.ssh
    chmod 600 $KEYPATH
    chmod 600 $CERT
  fi
  CMD="ssh-copy-id -i $CERT $USER@$IP"
  CMD2="exit 0"
else 
  CMD="ssh -i $KEYPATH  $IP"
  CMD2="./menu.sh $INI"
fi
echo $CMD
$CMD
$CMD2
exit 0