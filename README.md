# Metamotion Web Controller #

Web interface that enables the user to control the collection of data with  MetaMotionR sensor, from Mbientlab.
Is recommended to use this software with a Raspberry Pi. In order to convert your RPi in a gateway for the
MetaMotionR imus, you can run the file `provision/provision.sh`, all the information needed can be found in the
`provision` directory, is recommended to read the **README** file from the provision directory before continue reading. 

This web controller is formed by two application, once for stream the data in real time to th RPi and save them in a file, and the second create logs in the sensor, to save data locally in order to lately download all the data to the RPi.

In the streaming app, the work flow is the following:
1. Enter the name of the file where you want to store the collected information
2. Press the **Begin Measurement** button, and wait until the connection with the sensor is made, you will notice it because a green led will light up on the image.
3. To finish, press **Stop Measurement**, and wait for it to stop and store all data. Search your file in the path /home/pi/metamotion_files (if, in the RPi there must be a pi user, my fault, little flexibility, I just realized as I was writing this). If you use a MetaHub (the sensor gateway) this user is the default one.

In the logging app the procedure is a bit different:
1. Press the button **Init Logs** in order to create loggers in the sensor
2. After waiting the desired time, introduce the file where the data must be saved and press the button **Download Logs**

Both apps are prepare to work with only **ONE METAMOTIONR SENSOR**, in future versiones is expected to extend this funcionality.