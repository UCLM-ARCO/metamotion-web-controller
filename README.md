Web interface that enables the user to control the collection of data with  MetaMotionR sensor, from Mbientlab.
Is recommended to use this software with a Raspberry Pi. In order to convert your RPi in a gateway for the
MetaMotionR imus, you can run the file provision/provision.sh, which can be found in this repo. Following, 
if you connect to the port 8000, you can see the two main applications to save data in files (streaming the 
data or logging it in the sensor for its later download). The files where the data is saved, can be found 
in the path ~/metamotion_files.