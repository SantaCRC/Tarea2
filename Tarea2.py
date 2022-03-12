import threading
import time
import argparse
import RPi.GPIO as GPIO

## Se configuran los pines GPIO de la Raspberry Pi
GPIO.setmode (GPIO.BOARD) 
ledPin = 12
buttonPin = 16
GPIO.setup (ledPin, GPIO.OUT) 
GPIO.setup (buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

## Se definen el argumento para el parametro que sera introducido
## en el shell de Linux
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inp", type=int, help="Inp")
arg = parser.parse_args()

suma=0

## Funcion que crea el arreglo de "x" cantidad de elementos desde 
## 0 hasta "x-1"
def Arreglo (x):
    cont=0
    arreglo_de_salida=[]
    while cont <= x:
        arreglo_de_salida.append(cont)
        cont=cont+1
    return arreglo_de_salida

## Funcion que eleva al cuadrado cada elemento del arreglo y
## realiza la sumatoria de todos los elementos. Incluye el retardo entre
## iteraciones de 0.1 segundos solicitado por el enunciado. 
def Potencia_por_elemento (Arreglo):
    global suma
    arreglo_salida=[]
    for i in range (len(Arreglo)):
        suma=Arreglo[i]**2+suma
        time.sleep(0.1)
    return suma

## Funcion que separa el arreglo en "n" cantidad de partes con la
## misma cantidad de elementos cada parte
def Separar_Lista (Arreglo, size):
    return [Arreglo[i::size] for i in range(size)]

## Funcion principal que utiliza las funciones anteriormente descritas
## Crea el arreglo, realiza el procedimiento para 1 hilo, separa el arreglo
## Y realiza el procedimiento para 4 hilos, midiendo el tiempo en los dos
## Procedimientos para evaluar la rapidez de cada uno.
def Hilos(x):
    global suma
    # Para 1 Hilo
    Arreglo1=Arreglo(x)
    
    hilo1=threading.Thread(target=Potencia_por_elemento, args=(Arreglo1,)) ## Crea
    ## 1 hilo y ejectuta la funcion Potencia_por_elemento sobre el Arreglo
    ## introducido como argumento
    start1=time.time() ## Se guarda en una variable el tiempo de inicio
    hilo1.start() ## Inicia el hilo  
    hilo1.join() ## Espera que el hilo termine el procedimiento
    end1=time.time()  ## Se guarda en otra variable el tiempo de finalizacion 
    print("Tiempo de ejecucion de 1 hilo: {} con suma {} ".format(end1-start1,suma))
    ## Se imprime el tiempo de ejecucion (tiempo final - inicial) y el resultado
    ## del procedimiento
    

    # Para 4 hilos
    suma=0
    ArregloDiv = Separar_Lista(Arreglo1,4) ## Divide el arreglo en 4 partes
    hilo1 = threading.Thread(target=Potencia_por_elemento, args=(ArregloDiv[0],))
    hilo2 = threading.Thread(target=Potencia_por_elemento, args=(ArregloDiv[1],))
    hilo3 = threading.Thread(target=Potencia_por_elemento, args=(ArregloDiv[2],))
    hilo4 = threading.Thread(target=Potencia_por_elemento, args=(ArregloDiv[3],))
    ## Crea los 4 hilos encargados de ejecutar la funcion Portencia_por_elemento
    ## sobre cada una de las 4 partes correspondientes.
    
    start2=time.time() ## Se guarda en una variable el tiempo de inicio
    hilo1.start() ## Se inician todos los hilos
    hilo2.start()
    hilo3.start()
    hilo4.start()

    hilo1.join() ## Se espera a que todos los hilos terminen su procedimiento
    hilo2.join()
    hilo3.join()
    hilo4.join()

    end2=time.time() ## Se guarda en otra variable el tiempo de finalizacion

    print("Tiempo de ejecucion de 4 hilos: {} con suma {} ".format(end2-start2,suma))
    ## Se imprime el tiempo de ejecucion y el resultado del procedimiento
    suma = 0

## While encargado de ejectutar la funcion principal cuando se presione el pin
## GPIO de la Raspberry Pi
while True: 
    buttonState = GPIO.input (buttonPin) 
    if buttonState == False:
        print("Button Pressed")
        Hilos(arg.inp)
        GPIO.output (ledPin, GPIO.HIGH)                
    else: 
        GPIO.output (ledPin, GPIO.LOW)
