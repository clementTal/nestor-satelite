# TELEINFO MQTT

## Préparation du pi
1. wifi et ssh:

Ajouter le contenu du dossier boot dans le pi (après avoir modifié les variables du fichier `wpa_supplicant.conf`)
  
2. desactivation du serial
```
sudo raspi-config
```
* 5 interfacing option
  * P6 Serial
    * no
    * yes
  
3. ajout des packages
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install  --yes --force-yes  samba samba-common-bin python-pip
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.old
``` 
 
4. configuration de samba (optionel)
  ```
  sudo smbpasswd -a pi
  sudo nano /etc/samba/smb.conf
  ```
  * Ajouter
  ```
  [teleinfo]
  comment = teleinfo
  path = /home/pi/
  writable = yes
  guest ok = no
  guest only = no
  create mode = 0777
  directory mode = 0777
  share modes = yes
  ```  
  * Enregistrer
  `sudo systemctl restart smbd.service`
   
5. Ajout des lib python
`sudo pip install pyserial paho-mqtt`
    
## Installation du script

* Création du fichier
`mkdir /home/pi/teleinfo.py`
`vi /home/pi/teleinfo.py`

* copie du script et modification des variables MQTT
`python /home/pi/teleinfo.py`
==> OK/NOK

## Création du service
```
cd /lib/systemd/system/
sudo cp /home/pi/teleinfo/teleinfo.service  ./teleinfo.service
sudo chmod 644 teleinfo.service

sudo systemctl daemon-reload
sudo systemctl enable teleinfo.service
sudo systemctl start teleinfo.service
```


# bluetooth low energy [WIP]

## install service
http://www.instructables.com/id/Control-Bluetooth-LE-Devices-From-A-Raspberry-Pi/

