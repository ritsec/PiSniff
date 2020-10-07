# How to Connect Raspberry Pi Zero W to WPA2 Enterprise Network
#### Edit /etc/network/interfaces
```
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0

iface wlan0 inet dhcp
        pre-up wpa_supplicant -B -Dwext -i wlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
        post-down killall -q wpa_supplicant
```

#### Generate hashed password to put into wpa_supplicant.conf
```
sudo su
echo -n {password} | iconv -t utf16le | openssl md4 >> /etc/wpa_supplicant/wpa_supplicant.conf
```
This will put a has appended to your ```wpa_supplicant.conf``` file which you can now backspace and move on to the end of your network configuration explained below.

#### Edit /etc/wpa_supplicant/wpa_supplicant.conf
```
network = {
	ssid="RIT"
	key_mgmt=WPA-EAP
	eap=PEAP
	identity={username}
	phase1="peaplabel=0"
	phase2="auth=MSCHAPV2"
	priority=1
	password=hash:{hash_generated_from_last_step}
}
```
