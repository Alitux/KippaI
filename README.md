KIPPA I
=======

Kippa I es un ROV (Vehículo Operado Remotamente) orientado a inspección de cascos, hélices y timones de buques, veleros, etc.
El mismo está desarrollado enteramente con Software y Hardware Libre.

La comunicación entre el cliente(operador) y el ROV se realiza mediante UDP.
Por cuestiones de latencia la transmisión de imágenes se realiza mediante cable coaxil. La misma puede ser digitalizada mediante capturadora. En nuestro caso utilizamos una EasyCAP(05e1:0408 Syntek Semiconductor Co., Ltd STK1160 Video Capture Device) con resultados mas que satisfactorios. También se podría utilizar un monitor o cualquier pantalla con entrada RCA.


### Descripción de contenido ###

* Carpeta Arduino: Firmware desarrollado para Arduino Mega. Recibe los paquetes UDP y activa los distintos componentes.
* Carpeta Cliente: Software para el control del ROV ejecutado del lado cliente. También tiene capacidad de recibir el video de la capturadora.

## Funciones a implementar ##

- Captura de fotografía (Cliente)
- Volcado de video en un archivo local (Cliente)
- Medición de latencia (Cliente)