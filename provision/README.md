Ejecutando el script sh aquí presente puedes convertir una RPi en un punto de acceso
que recolectará datos de un sensor MetaMotionR via una interfaz web. Los pasos necesarios son
los siguientes

1. Copia este directorio en una RPi
2. Ejecuta el archivo provision.sh para realizar la provision con permisos de superusuario `sudo ./provision.sh`
3. Espera a que termine la provisión
4. Si todos los pasos han terminado correctamente reiniciar la RPi
5. Al iniciar, nuestra RPi será un AP con el SSID Raspberry y con la contraseña password
6. Una vez conectado a la RPi, introducir en el navegador `192.168.4.1:8000`, se mostrará la interfaz web para capturar datos con el sensor
7. Introducir el nombre del archivo donde se quiera almacenar la información recolectada
8. Pulsar el botón **Begin Measurement**, y esperar hasta que se produzca la conexión con el sensor, lo notarás porque en el imu se encenderá un led verde.
9. Para finalizar pulsa el botón **Stop Measurement**, y espera a que se detenga y almacenen todos los datos. Buscar tu archivo en la ruta /home/pi/metamotion_files (si, en la RPi debe haber un usuario pi, fallo mío, poca flexibilidad, me acabo de dar cuenta conforma escribía esto). Si se usa un MetaHub (el gateway de los sensores) este usuario es el que hay por defecto.


