to install use our shell script

 URL= https://raw.github.com/atelier-it-ro/metrics-collector/main/install.sh && if [ -f /usr/bin/curl ];then curl -ksSO "$URL" ;else wget install.sh "$URL";fi;bash install.sh
