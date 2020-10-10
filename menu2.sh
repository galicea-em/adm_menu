#!/bin/bash

HEIGHT=25
WIDTH=40
CHOICE_HEIGHT=15
BACKTITLE="Wybór opcji"
TITLE="Serwery"
MENU="Wybierz serwer:"

OPTIONS=(1 "10.0.0.116"
         9 "poprzednia strona"
         )

CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear
case $CHOICE in
        1)
            ssh 10.0.0.116;./menu2.sh
            ;;
        9)
            ./menu.sh
            ;;
esac