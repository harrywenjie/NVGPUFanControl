# Auto Fan Curve Under Linux.

I use this code myself under Linux.  

The fan speed is 50% when the temperature is below 40 degrees. Between 40 and 50 degrees, the fan speed gradually increases from 50% to 60%. Above 50 degrees, the fan speed gradually increases from 60% to 100% as the temperature increases to 80 degrees. If the temperature exceeds 80 degrees, the fan speed is capped at 100%.

The min(int(speed), 100) line ensures that the fan speed does not exceed 100%, even if the temperature is above 80 degrees.

---

### 1. Edit xorg.conf

```bash
sudo nvidia-xconfig
sudo nano /etc/X11/xorg.conf
```
Enable Coolbits
```conf
Section "Device"
    Identifier     "Device0"
    Driver         "nvidia"
    VendorName     "NVIDIA Corporation"
    Option         "Coolbits" "4"
EndSection
```

### 2. Set it as systemd service

find path of autofan.py , for example
```bash
~/NVGPUFanControl/autofan.py
```

Create a systemd service file: Open a new file in /etc/systemd/system/  

```bash
sudo nano /etc/systemd/system/gpufancontrol.service
```
Then add the following content to the file,   
use your own path to the script
```bash
[Unit]
Description=GPU Fan Control

[Service]
ExecStart=/usr/bin/python3 /path/to/autofan.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

Enable the service: Enable the service to start on boot:  
```bash
sudo systemctl enable gpufancontrol
```

Start the service: Start the service immediately:  
```bash
sudo systemctl start gpufancontrol
```

### 3. Allow root to connect to X server
```bash
xhost +SI:localuser:root
```
To make it permanent, Add the above line to this file below.
```
nano ~/.xinitrc
```



### 4. Finished but you can check status with bash  
```bash
sudo systemctl status gpufancontrol
```