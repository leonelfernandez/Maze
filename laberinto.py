from pila import *
import random
from mapa import Mapa, Coord

def generar_laberinto(filas, columnas):
    """Generar un laberinto.

    Argumentos:
        filas, columnas (int): Tamaño del mapa

    Devuelve:
        Mapa: un mapa nuevo con celdas bloqueadas formando un laberinto
              aleatorio
    """
    
    camino = Pila()
    celdas_visitadas = []
    mapa = Mapa(filas, columnas)
    mapa.bloquear_todo()
    camino.apilar(mapa.origen())
    celdas_visitadas.append(mapa.origen())
    mapa.desbloquear(mapa.origen())
    
    def backtrack(camino, celdas_visitadas, mapa):
        celdas_a_elegir = []
        celda = camino.ver_tope()

        for celda_vecina in mapa.obtener_vecinos_pares(celda):
            if not celda_vecina in celdas_visitadas:
                if celda_vecina.fila != 0 and celda_vecina.columna != 0:
                    if celda_vecina.fila != mapa.filas - 1 and celda_vecina.columna != mapa.columnas - 1:
                        celdas_a_elegir.append(celda_vecina)

        if not celdas_a_elegir == [] and mapa.destino() != celda:
            indice_aleatorio = random.randint(0, len(celdas_a_elegir) -1)        
            celda_aleatoria = celdas_a_elegir[indice_aleatorio]
            camino.apilar(celda_aleatoria)
            celdas_visitadas.append(celda_aleatoria)
            mapa.desbloquear(celda_aleatoria)
            celda_intermedia = celda.obtener_celda_intermedia(celda_aleatoria)
            mapa.desbloquear(celda_intermedia)
        else:
            camino.desapilar()

        return camino, celdas_visitadas
    
    while not camino.esta_vacia():
        camino, celdas_visitadas = backtrack(camino, celdas_visitadas, mapa)
        # try:
        #     camino, celdas_visitadas = backtrack(camino, celdas_visitadas, mapa)
        # except:
        #     raise Exception(f"excepcion al generar laberinto:{camino} {celdas_visitadas}")

    mapa.desbloquear(mapa.destino())
    return mapa
    