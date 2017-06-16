#!/bin/sh

ocreadvalue=`sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq`
ocvalue="700000"
freq=`grep arm_freq /boot/config.txt`
spistatus=`grep spi-bcm2708 /etc/modprobe.d/*-blacklist.conf`
clear
echo "====================================================="
echo "====================================================="
echo "---My Sensors installer for NRF24l01 GPIO Support ---"
echo "====================================================="
echo "====================================================="
echo ""
echo ""
echo ""
echo ""
echo ""
echo "====================================================="
echo "=============Verifying Overclock Status=============="
echo "====================================================="
echo ""

if [ "$ocvalue" -eq "$ocreadvalue" ]; then
	echo "      [OK]    No Overclock detected."
        echo ""
else
	echo "             Your rPi is Overclocked."
        echo "        Do you want me to fix that for you?"
        echo ""
	read -p "   Answer by pressing y for Yes or n for No =======>" RESP
	if [ "$RESP" = "y" ]; then
		sudo sed -i 's/'"$freq"'/arm_freq=700/g' /boot/config.txt
		echo ""
		echo "   `sudo cat /boot/config.txt | grep arm_freq=`"
		echo "   Done!"
	else
		echo "   Ok, but SPI will not work"
	fi
fi

echo ""
echo "====================================================="
echo "===========Veryfing if SPI is Blacklisted============"
echo "====================================================="
echo ""
line=$(grep -w "#blacklist spi-bcm2708" /etc/modprobe.d/*-blacklist.conf)
if [ $? -eq 1 ]; then
	echo "              SPI is in the Blacklist"
        echo "        Do you want me to fix that for you?"
        echo ""
        read -p "   Answer by pressing y for Yes or n for No =======>" RESP
        if [ "$RESP" = "y" ]; then
                file=`grep -l "blacklist spi-bcm2708" /etc/modprobe.d/*-blacklist.conf`
                sed --quiet -i '/blacklist spi-bcm2708/d' "$file"
		echo "#blacklist spi-bcm2708" >> "$file"
                echo ""
                echo "   `sudo cat $file`"
                echo "   Done!"
        else
                echo ""
                echo "   Ok, but SPI will not work"
        fi

else
	echo "      [OK]    SPI is NOT in the Blacklist"
fi

echo ""
echo "====================================================="
echo "=========Veryfing if SPI is enabled on boot=========="
echo "====================================================="
echo ""
line2=$(grep -w "dtparam=spi=on" /boot/config.txt)
if [ $? -eq 1 ]; then
        echo "              SPI is not enabled on boot"
        echo "        Do you want me to fix that for you?"
        echo ""
        read -p "   Answer by pressing y for Yes or n for No =======>" RESP
        if [ "$RESP" = "y" ]; then
                echo "dtparam=spi=on" >> /boot/config.txt
                echo ""
                echo "   Done!"
        else
                echo ""
                echo "   Ok, but SPI will not work"
        fi

else
        echo "      [OK]    SPI is enabled on boot"
fi

echo ""
echo "====================================================="
echo "===== Downloading and Installing what you need ======"
echo "====================================================="
echo ""
read -p "Tell me where do you want your files (ex: /home/pi/)" RESP
echo "Donwloading to $RESP using wget"
if [ -d "$RESP" ]; then
cd "$RESP"
else
mkdir "$RESP"
cd "$RESP"
fi
wget https://github.com/mysensors/Raspberry/archive/master.zip
command -v unzip  >/dev/null 2>&1 || { echo >&2 "I need unzip.. Installing "; sudo apt-get -y install unzip; }
unzip master.zip -d "$RESP"
rm master.zip
cd Raspberry-master/librf24-bcm
make
cd ..
make
clear
echo ""
echo "Done!"
echo ""
echo "====================================================="
echo "============== Connect your NRF24l01 ================"
echo "====================================================="
echo ""
echo "PIN     NRF24L01    RPI             RPi -P1 Connector"
echo "1       GND         rpi-gnd         (25)"
echo "2       VCC         rpi-3v3         (17)"
echo "3       CE          rpi-gpio22      (15)****"
echo "4       CSN         rpi-gpio8       (24)"
echo "5       SCK         rpi-sckl        (23)"
echo "6       MOSI        rpi-mosi        (19)"
echo "7       MISO        rpi-miso        (21)"
echo "8       IRQ         Not Connected"
echo ""
echo "***DO NOT CONNECT THE CE PIN***"
echo "!Read below where to connect your CE Pin!"
echo ""
read -p "Press any key after you are done" RESP
echo ""
echo "====================================================="
echo "============ Starting PiGateway Serial =============="
echo "====================================================="
echo ""
./PiGatewaySerial &


