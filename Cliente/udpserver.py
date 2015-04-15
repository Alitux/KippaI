##!/usr/bin/env python
## -*- coding: utf-8 -*-
# UDPServer lo usamos unicamente para probar al cliente. Dejo el código medio
# chancho solo por si a alguien le parece util
import socket
import select
import time
UDP_IP="0.0.0.0" # Recibir de cualquier cliente
UDP_PORT=3400 #Puerto de conexion
UDP_HOST = "10.30.121.113" #IP del ROV

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # Inet e UDP

sock.bind( (UDP_IP,UDP_PORT) )
# Pone el socket en modo de no bloqueo,
# evitando poner a recv en bucle infinito si no hay datos en el buffer
sock.setblocking(0)

def envio_paquetes(mensaje):
    ##INICIO ENVIO DE PAQUETES ##
    mensaje=mensaje
    # No hay comandos locales, manda el texto al remoto
    print mensaje
    sock.sendto(mensaje, (UDP_HOST, UDP_PORT))
    ##FIN ENVIO DE PAQUETES##

def recepcion_paquetes():
    ##INICIO RECEPCION DE PAQUETES##
    # Valida si recibe algo por el socket
    HayDatosSocket = select.select([sock],[],[],0.5)
    if HayDatosSocket[0]:
        Socketdata  = sock.recv( 1024 ) # buffer size is 1024 bytes
        return Socketdata
    HayDatosSocket = []
    ##FIN RECEPCION DE PAQUETES##
# envio_paquetes("luces_encendidas")
while True:
    time.sleep(1)
    envio_paquetes(str(1))