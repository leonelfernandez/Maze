import random
from mapa import Coord
from pila import *

class IA:
    """
    Inteligencia artificial para resolver un laberinto.

    Se simula un jugador que comienza en la celda de origen, y mediante
    el método avanzar() el jugador hace un movimiento.

    Ejemplo:
        >>> mapa = Mapa(10, 10)
        >>> ia = IA()
        >>> ia.coord_jugador()
        Coord(0, 0)
        >>> while ia.coord_jugador() != mapa.destino()
        ...     ia.avanzar()
        >>> ia.coord_jugador()
        Coord(9, 9)
    """

    def __init__(self, mapa):
        """Constructor.

        Argumentos:
            mapa (Mapa): El mapa con el laberinto a resolver
        """
        self.mapa = mapa
        self.coord_actual_jugador = mapa.origen()
        self.celdas_visitadas = []
        self.camino_actual = Pila()
        self.camino_actual.apilar(self.mapa.origen())
        self.celdas_visitadas.append(self.mapa.origen())
        self.camino_lista = []
    def coord_jugador(self):
        """Coordenadas del "jugador".

        Devuelve las coordenadas de la celda en la que se encuentra el jugador.

        Devuelve:
            Coord: Coordenadas del "jugador"

        Ejemplo:
            >>> ia = IA(Mapa(10, 10))
            >>> ia.coord_jugador()
            Coord(0, 0)
            >>> ia.avanzar()
            >>> ia.coord_jugador()
            Coord(1, 0)
            >>> ia.avanzar()
            >>> ia.coord_jugador()
            Coord(2, 0)
        """
        return self.coord_actual_jugador
        
        

    def visitados(self):
        """Celdas visitadas.

        Devuelve:
            secuencia<Coord>: Devuelve la lista (o cualqueir otra secuencia) de
            de celdas visitadas al menos una vez por el jugador desde que
            comenzó la simulación.

        Ejemplo:
            >>> ia = IA(Mapa(10, 10))
            >>> ia.avanzar()
            >>> ia.avanzar()
            >>> ia.avanzar()
            >>> ia.visitados()
            [Coord(0, 0), Coord(1, 0),  Coord(2, 0)]
        """
        return self.celdas_visitadas

    def camino(self):
        """Camino principal calculado.

        Devuelve:
            secuencia<Coord>: Devuelve la lista (o cualqueir otra secuencia) de
            de celdas que componen el camino desde el origen hasta la posición
            del jugador. Esta lista debe ser un subconjunto de visitados().

        Ejemplo:
            >>> ia = IA(Mapa(10, 10))
            >>> for i in range(6):
            ...     ia.avanzar()
            >>> ia.visitados()
            [Coord(0, 0), Coord(1, 0), Coord(1, 1),  Coord(2, 0),  Coord(3, 0),  Coord(4, 0)]
            >>> ia.camino()
            [Coord(0, 0), Coord(1, 0),  Coord(2, 0),  Coord(3, 0),  Coord(4, 0)]

        Nota:
            La celda actual en la que está el jugador puede no estar en la
            lista devuelta (esto tal vez permite simplificar la
            implementación).
        """
        return self.camino_lista

    def avanzar(self):
        """Avanza un paso en la simulación.

        Si el jugador no está en la celda destino, y hay algún movimiento
        posible hacia una celda no visitada, se efectúa ese movimiento.
        """
   
        celdas_a_elegir = []
        if self.camino_actual.esta_vacia():
            return

        celda = self.camino_actual.ver_tope()

        if self.mapa.destino() == celda:
            return 

        for celda_vecina in self.mapa.obtener_vecinos(celda):
            if not celda_vecina in self.celdas_visitadas:
                if not self.mapa.celda_bloqueada(celda_vecina):
                    celdas_a_elegir.append(celda_vecina)

        if not celdas_a_elegir == []:
            indice_aleatorio = random.randint(0, len(celdas_a_elegir) -1)        
            celda_aleatoria = celdas_a_elegir[indice_aleatorio]
            self.camino_actual.apilar(celda_aleatoria)
            self.camino_lista.append(celda_aleatoria)
            self.celdas_visitadas.append(celda_aleatoria)
            self.coord_actual_jugador = celda_aleatoria
        else:
            self.camino_actual.desapilar()
            self.camino_lista.pop()
            self.coord_actual_jugador = self.camino_actual.ver_tope()
        
        
              
    

    

    

         
