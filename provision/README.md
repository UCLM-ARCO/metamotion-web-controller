Executing the sh script here you can turn an RPi into an access point
which will collect data from a MetaMotionR sensor via a web interface. The necessary steps are
the following

1. Clone this repository into a RPi
2. Run provision.sh file with superuser permissions `sudo ./provision.sh`.
3. Wait for the provision to end
4. If all the steps have been completed correctly, restart the RPi
5. When starting, our RPi will be an AP with the SSID Raspberry and the password
6. Once connected to the RPi, we can use two apps in the links `192.168.4.1:8000/streaming` and `192.168.4.1:8000/logging`, the first stream the data in real time to th RPi and save them in a file, the second create logs in the sensor, to save data locally in order to lately, download all the data to the RPi.