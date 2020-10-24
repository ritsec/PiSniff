# How to Connect Raspberry Pi Zero W to WPA2 Enterprise Network with USB NIC
#### Step 1: Edit /etc/network/interfaces
```
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0

iface wlan0 inet dhcp
        pre-up wpa_supplicant -B -Dwext -i wlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
        post-down killall -q wpa_supplicant
```

#### Step 2: Generate hashed password to put into wpa_supplicant.conf
```
sudo su
echo -n {password} | iconv -t utf16le | openssl md4 >> /etc/wpa_supplicant/wpa_supplicant.conf
```
This will put a has appended to your ```wpa_supplicant.conf``` file which you can now backspace and move on to the end of your network configuration explained below.

#### Step 3: Edit /etc/wpa_supplicant/wpa_supplicant.conf
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

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

#### Step 4: Reboot Pi
```sudo reboot now```

#### Step 5: Check connection
```ping 8.8.8.8```

#### Step 6: Get IP of wlan0 (internal NIC) to connect using ssh
```
tracker@tracker4:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 9c:ef:d5:fa:12:e4 brd ff:ff:ff:ff:ff:ff
    inet 129.21.66.204/22 brd 129.21.67.255 scope global dynamic wlan0
       valid_lft 1576sec preferred_lft 1576sec
    inet6 2620:8d:8000:1040:9eef:d5ff:fefa:12e4/64 scope global dynamic mngtmpaddr
       valid_lft 2591998sec preferred_lft 604798sec
    inet6 fe80::9eef:d5ff:fefa:12e4/64 scope link
       valid_lft forever preferred_lft forever
```

The ip you will get from from looking at wlan0's inet address which in this case is ```129.21.66.204```

Record this because you will need it to SSH into the pi after the next step.

#### Step 7: Add your ssh public key to the pi so you can connect
1. Open PowerShell in your home directory
2. ```ssh-keygen -t ed25519```
3. It may ask you to enter a password to be used with the key, use at your own discretion.
3. This should generate a public and private key named (by default) as ```id_ed25519``` and ```id_ed25519.pub```
4. Upload your public key ```id_ed25519.pub``` to pastebin.com
5. On the pi navigate to your .ssh directory ```cd ~/.ssh```
6. On your pi now run ```wget https://pastebin.com/raw/{your_pastebin_code}``` which will download your public key to a file named ```{your_pastebin_code}```
7. Now, append the downloaded public key file to the ```authorized_keys``` file using ```cat {your_pastebin_code} >> authorized_keys```
8. Remove the newline at the end of ```authorized_keys``` using ```nano authorized_keys``` and remove the newline from the end of the file and save it.
9. Now your pi is ready for SSH!

#### Step 8: Modify /etc/network/interfaces to add wlan1 temporarily to setup USB NIC
Add a repeat of what you wrote for wlan0 except replace all instances of wlan0 with wlan1.
Your file should look like this:
```
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
allow-hotplug wlan1

iface wlan0 inet dhcp
        pre-up wpa_supplicant -B -Dwext -i wlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
        post-down killall -q wpa_supplicant
	
iface wlan1 inet dhcp
        pre-up wpa_supplicant -B -Dwext -i wlan1 -c/etc/wpa_supplicant/wpa_supplicant.conf
        post-down killall -q wpa_supplicant
```


#### Step 9: Shutdown the pi and SSH into it from another computer
```shutdown now```

Now plug the USB NIC into the USB port instead of your keybord.

When done, unplug then plug back in your pi power supply to power on the pi again.

When it is done booting up you should be able to ssh into the pi from your personal computer.

Connect using ```ssh tracker@{your_pi_ip_from_step_6} -p 49222``` (Note: the port should already be set to 49222, but if that doesn't work just use ssh without the ```-p 49222```

You should now be connected to the pi.

Now we can setup the USB NIC!

#### Step 10: Register NIC with start.rit.edu so we can use a hostname from now on instead of the dynamic IP
```iwconfig```
You should see wlan0 and wlan1 both connected to RIT, this is good.

```ip a```
You should see the mac address for wlan1 on the line that says ```link/ether xx:xx:xx:xx:xx:xx```

On your desktop navigate to start.rit.edu

Click on "My Computers", then "Advanced Registration"

Type in the mac address from before and click register, it should be successful. Now give it a hostname (preferably tracker{#}) and fill in the additional information.

You should now be able to connect to the pi using the hostname tracker{#}.student.rit.edu instead of the dynamic IP that we won't know unless we have access to the pi.

#### Step 11: Remove wlan1 from /etc/network/interface (revert step 8 back to step 1)
Restore ```/etc/network/interface``` to step 1 configuration (remove all wlan1 entries)
```
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0

iface wlan0 inet dhcp
        pre-up wpa_supplicant -B -Dwext -i wlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
        post-down killall -q wpa_supplicant
```



#### Step 12: Disable the onboard wifi then reboot
```
sudo su
echo "dtoverlay=disable-wifi" >> /boot/config.txt
reboot now
```

### Step 13: Connect to Pi on SSH through the USB NIC
Once the pi is booted connect to the pi using the same command from step 9 ```ssh tracker@{your_pi_ip_from_step_6} -p 49222``` except replace the ip with the new hostname ```ssh tracker@tracker{#}.student.rit.edu -p 49222```

### Done!



