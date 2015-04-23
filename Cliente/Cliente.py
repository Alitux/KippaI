#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------
# Importacion de los módulos
# ---------------------------
import pygame
from pygame.locals import *
from threading import Thread
import os
import sys
import socket
import select
import commands
from time import sleep
from SimpleCV import Camera, VideoStream
## Variables de conexion

UDP_IP="0.0.0.0" # Recibir de cualquier cliente
UDP_PORT=3400 #Puerto de conexion

UDP_HOST = "10.30.121.107" #IP del ROV

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # Inet e UDP

sock.bind( (UDP_IP,UDP_PORT) )
# Pone el socket en modo de no bloqueo,
# evitando poner a recv en bucle infinito si no hay datos en el buffer
sock.setblocking(0)

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
IMG_DIR = "Imagenes"

## Se definen los movimientos del ROV


# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print "Error, no se puede cargar la imagen: ", ruta
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

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

def latencia():
    global r_latencia
    r_latencia=""
    while True:
        pingueo=commands.getoutput("ping -q -c2 "+str(UDP_HOST))
        #pingueo=commands.getoutput("ping -q -c4 "+str("www.google.com.ar")) #Para pruebas
        try:
            latencia=pingueo.split("/")[4] #Se extrae latencia
            r_latencia=latencia
            time.sleep(5)
        except IndexError:
            r_latencia="SINRTA!"

# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:



class Luces(pygame.sprite.Sprite):
    "Luces"

    def __init__(self):
        self.estado_luces=False
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("luces_encendidas.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect() #Se obtiene un objeto rect para coordenadas y tamaño
        self.rect.centerx = 1037 #Posición en X
        self.rect.centery = 259 #Posición en Y


class Flecha(pygame.sprite.Sprite):
    "Creador de Flechas"
    def __init__(self, imagene, imagena, posx, posy):
        self.posx=posx
        self.posy=posy
        self.activada=False
        self.imagene=imagene
        self.imagena=imagena
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(self.imagene, IMG_DIR, alpha=True)
        self.rect = self.image.get_rect() #Se obtiene un objeto rect para coordenadas y tamaño
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
    def estado(self, status):
        if status==True:
            self.image = load_image(self.imagene, IMG_DIR, alpha=True)
            self.activada=True
        else:
            self.image = load_image(self.imagena, IMG_DIR, alpha=True)
            self.activada=False

class Profundidad(pygame.sprite.Sprite):
    "Timon de profundidad"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("mando_profundidad.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect() #Se obtiene un objeto rect para coordenadas y tamaño
        self.rect.centerx = 507 #Posición en X
        self.rect.centery = 656 #Posición en Y
    def posicion(self, pos):
        self.pos=pos
        if self.pos=="descender":
            self.rect.centery = 716 #Posición en Y
        if self.pos=="neutral":
            self.rect.centery = 656 #Posición en Y
        if self.pos=="ascender":
            self.rect.centery=596 #Posición en Y

class Motor(pygame.sprite.Sprite):
    "Motor Central"
    def __init__(self, imagene, imagena, posx, posy):
        self.posx=posx
        self.posy=posy
        self.activada=False
        self.imagene=imagene
        self.imagena=imagena
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(self.imagene, IMG_DIR, alpha=True)
        self.rect = self.image.get_rect() #Se obtiene un objeto rect para coordenadas y tamaño
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
    def estado(self, status):
        if status==True:
            self.image = load_image(self.imagene, IMG_DIR, alpha=True)
            self.activada=True
        else:
            self.image = load_image(self.imagena, IMG_DIR, alpha=True)
            self.activada=False



class Camara(pygame.sprite.Sprite):
    "ImagenCamara"
    #TODO: Se debería mejorar la elección de cámara, así no se toca el código
    elegida=0 #Por defecto es la cámara 0 o /dev/video0
    estado=False #Estado de cámar(False=Apagada, True=Encendida)
    norma="PALN" #Norma(Hay que ver como se puede cambiar)
    cam=""
    def __init__(self):
        self.estado_luces=False
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("cam_principal_apagada.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect() #Se obtiene un objeto rect para coordenadas y tamaño
        self.rect.centerx = 385
        self.rect.centery = 280
        self.image=pygame.transform.scale(self.image, (640, 480))

    def encender(self):
        self.estado=True
        self.cam=Camera(self.elegida)
        #En esta sección se deben anexar las rutinas de encendido de camara
        #
        #
        #En esta sección se deben agregar el comportamiento de las gráficas
        #
        #
        #
    def apagar(self):
        if self.estado==True:
            del self.cam
            self.estado=False

        #En esta sección se deben anexar las rutinas de apagado de camara
        #
        #
        #En esta sección se deben agregar el comportamiento de las gráficas
        #
        #
        #

    def obtener_imagen(self): #Se obtiene imagen en formato SimpleCV

        if self.estado==True:
            imagen=self.cam.getImage().toPygameSurface()
        else:
            imagen=SimpleCV.Image("Imagenes/cam_principal_apagada.png").toPygameSurface()
        return imagen

    def sacar_foto(self,archivo): #OPTIMIZE: Es necesario mejorar esta función
        self.archivo=archivo
        imagen=self.cam.getImage()
        imagen.save(archivo)

    #TODO: Trabajar sobre la función de volcado de video a un archivo




# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    retroceso=False
    avante=False
    babor=False
    estribor=False
    ascenso=False
    descenso=False

    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kippa I V1.00")
    coordenadas=pygame.mouse.get_pos()
    #pygame.display.toggle_fullscreen()
    # cargamos los objetos
    fondo = load_image("fondo_1366x768.png", IMG_DIR, alpha=False)
    letra20 = pygame.font.SysFont("Arial", 20)
    texto_coordenadas = letra20.render(str(coordenadas), True, (200,200,200), (0,0,0) )

    luces=Luces()
    ##Creación de flechas y timón de profundidad
    izquierda=Flecha("izquierda_encendida.png","izquierda_apagado.png",106,632)
    derecha=Flecha("derecha_encendida.png","derecha_apagado.png",170,632)
    arriba=Flecha("arriba_encendida.png", "arriba_apagado.png", 138,603)
    abajo=Flecha("abajo_encendida.png","abajo_apagado.png",138,659)
    timon_profundidad=Profundidad()

    ##Creación de motores
    motor_central_izquierdo=Motor("motor_central_encendido.png","motor_central_apagado.png",932,339)
    motor_central_derecho=Motor("motor_central_encendido.png","motor_central_apagado.png",1149,339)
    motor_trasero_izquierdo=Motor("motor_trasero_encendido.png","motor_trasero_apagado.png",951,443)
    motor_trasero_derecho=Motor("motor_trasero_encendido.png","motor_trasero_apagado.png",1137,443)



    camara_principal=Camara() #Se crea una representacion de la cámara
    camara_principal.encender() #Se enciende la cámara
    pygame.key.set_repeat(10, 50) #Se regula la velocidad de repetición
    clock=pygame.time.Clock()
    # Se reestablece el estado a False de todas las flechas
    izquierda.estado(False)
    derecha.estado(False)
    arriba.estado(False)
    abajo.estado(False)
    timon_profundidad.posicion("neutral")
    ## False en todos los motores
    motor_central_izquierdo.estado(False)
    motor_central_derecho.estado(False)
    motor_trasero_izquierdo.estado(False)
    motor_trasero_derecho.estado(False)
    # el bucle principal del juego
    t_latencia=""
    Thread(target=latencia,).start()
    while True:
        screen.blit(fondo,(0,0))
        clock.tick(10)
        ##INICIO Medición de latencia
        thr_latencia=Thread(target=latencia,).start()
        #Se obtienen valores de latencia
        if r_latencia=="": #Si no existe nada, se queda el anterior
            t_latencia=t_latencia
        else: #Si existe, se reemplaza por el nuevo
            t_latencia=str(r_latencia)+" ms"
        ##FIN Medición de Latencia
        texto_coordenadas = letra20.render(str(pygame.mouse.get_pos()), True, (200,200,200), (0,0,0) )
        texto_latencia = letra20.render(str(t_latencia), True, (255,255,255))
        texto_host = letra20.render(str("UDP")+str(UDP_HOST)+str(":")+str(UDP_PORT), True, (255,255,255))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if keys[K_DOWN]:
                if retroceso==False:
                    retroceso=True
                    envio_paquetes(str(-8))
                    envio_paquetes(str(2)) ##Se envía Instrucciones al ROV
                    abajo.estado(True) #Estado de la Flecha
                    #Se evita la contradicción de estado
                    arriba.estado(False)
                    derecha.estado(False)
                    izquierda.estado(False)

                    motor_trasero_derecho.estado(True) #Estado del Motor
                    motor_trasero_izquierdo.estado(True) #Estado del Motor
                elif retroceso==True:
                    envio_paquetes(str(-8))
                    envio_paquetes(str(-2)) ##Se envía Instrucciones al ROV
                    abajo.estado(False) #Estado de la Flecha
                    #Se evita la contradicción de estado
                    arriba.estado(False)
                    derecha.estado(False)
                    izquierda.estado(False)

                    motor_trasero_derecho.estado(False) #Estado del Motor
                    motor_trasero_izquierdo.estado(False) #Estado del Motor
                    retroceso=False

            if keys[K_UP]:
                if avante==False:
                    avante=True
                    envio_paquetes(str(-8))
                    envio_paquetes(str(3))
                    arriba.estado(True)
                    #Se evita la contradicción de estado
                    abajo.estado(False)
                    derecha.estado(False)
                    izquierda.estado(False)

                    motor_trasero_derecho.estado(True)
                    motor_trasero_izquierdo.estado(True)

                elif avante==True:
                    avante=False
                    envio_paquetes(str(-8))
                    envio_paquetes(str(-3))
                    arriba.estado(False)
                    #Se evita la contradicción de estado
                    abajo.estado(False)
                    derecha.estado(False)
                    izquierda.estado(False)

                    motor_trasero_derecho.estado(False)
                    motor_trasero_izquierdo.estado(False)

            if keys[K_RIGHT]:
                if estribor==False:
                    estribor=True
                    envio_paquetes(str(-8))
                    envio_paquetes(str(4))
                    derecha.estado(True)
                    #Se evita la contradicción de estado
                    abajo.estado(False)
                    arriba.estado(False)
                    izquierda.estado(False)

                    motor_trasero_izquierdo.estado(True)
                elif estribor==True:
                    estribor=False
                    envio_paquetes(str(-8))
                    envio_paquetes(str(-4))
                    derecha.estado(False)
                    izquierda.estado(False)
                    #Se evita la contradicción de estado
                    abajo.estado(False)
                    arriba.estado(False)
                    izquierda.estado(False)

                    motor_trasero_izquierdo.estado(False)

            if keys[K_LEFT]:
                if babor==False:
                    babor=True
                    envio_paquetes(str(-8))
                    envio_paquetes(str(5))
                    izquierda.estado(True)
                    #Se evita la contradicción de estado
                    abajo.estado(False)
                    arriba.estado(False)
                    derecha.estado(False)

                    motor_trasero_derecho.estado(True)

                elif babor==True:
                    babor=False
                    envio_paquetes(str(-8))
                    envio_paquetes(str(-5))
                    izquierda.estado(False)
                    #Se evita la contradicción de estado
                    abajo.estado(False)
                    arriba.estado(False)
                    derecha.estado(False)

                    motor_trasero_derecho.estado(False)

            if keys[K_w]:
                if ascenso==False:
                    ascenso=True
                    envio_paquetes(str(-8))
                    envio_paquetes(str(6))
                    timon_profundidad.posicion("ascender")
                    motor_central_izquierdo.estado(True)
                    motor_central_derecho.estado(True)
                elif ascenso==True:
                    ascenso=False
                    envio_paquetes(str(-8))
                    envio_paquetes(str(-6))
                    timon_profundidad.posicion("neutral")
                    motor_central_izquierdo.estado(False)
                    motor_central_derecho.estado(False)

            if keys[K_s]:
                if descenso==False:
                    descenso=True
                    envio_paquetes(str(-8))
                    envio_paquetes(str(7))
                    timon_profundidad.posicion("descender")
                    motor_central_izquierdo.estado(True)
                    motor_central_derecho.estado(True)
                elif descenso==True:
                    descenso=False
                    envio_paquetes(str(-8))
                    envio_paquetes(str(-7))
                    timon_profundidad.posicion("neutral")
                    motor_central_izquierdo.estado(True)
                    motor_central_derecho.estado(True)


            if keys[K_l]:
                pygame.key.set_repeat(0, 0)
                if luces.estado_luces==True:
                    luces.estado_luces=False
                    envio_paquetes(str(0)) #TODO: Revisar este código. Puede estar invertido
                else:
                    luces.estado_luces=True
                    envio_paquetes(str(1)) #TODO: Revisar este código. Puede estar invertido

            if keys[K_r]:
                camara_principal.sacar_foto("Prueba.jpg")

            if keys[K_ESCAPE]:
                thr_latencia.exit()
                sys.exit()
                #TODO: Matar hilo de latencia que deja todo lento cuando no tiene respuesta
            if event.type == pygame.QUIT:
                sys.exit()


        #actualizamos la pantalla

        capturacamara=camara_principal.obtener_imagen()
        screen.blit(capturacamara, camara_principal.rect)

        ##Blitteo de flechas y timón de profundidad
        screen.blit(izquierda.image, izquierda.rect)
        screen.blit(derecha.image, derecha.rect)
        screen.blit(arriba.image, arriba.rect)
        screen.blit(abajo.image, abajo.rect)
        screen.blit(timon_profundidad.image, timon_profundidad.rect)
        ##Blitteo de motores
        screen.blit(motor_central_derecho.image, motor_central_derecho.rect)
        screen.blit(motor_central_izquierdo.image, motor_central_izquierdo.rect)
        screen.blit(motor_trasero_derecho.image, motor_trasero_derecho.rect)
        screen.blit(motor_trasero_izquierdo.image, motor_trasero_izquierdo.rect)




        if luces.estado_luces==True:
            screen.blit(luces.image, luces.rect)

        screen.blit(texto_coordenadas, (texto_coordenadas.get_rect()))
        screen.blit(texto_latencia, (1003,147))
        screen.blit(texto_host,(933,95))
        pygame.display.flip()




if __name__ == "__main__":
    main()
