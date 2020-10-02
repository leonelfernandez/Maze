class Coord:
    """
    Representa las coordenadas de una celda en una grilla 2D, representada
    como filas y columnas. Las coordendas ``fila = 0, columna = 0`` corresponden
    a la celda de arriba a la izquierda.

    Las instancias de Coord son inmutables.
    """

    def __init__(self, fila=0, columna=0):
        """Constructor.

        Argumentos:
            fila, columna (int): Coordenadas de la celda
        """
        self.fila = fila
        self.columna = columna

    def trasladar(self, df, dc):
        """Trasladar una celda.

        Devuelve una nueva instancia de Coord, correspondiente a las coordenadas
        de la celda que se encuentra ``df`` filas y ``dc`` columnas de distancia.

        Argumentos:
            df (int): Cantidad de filas a trasladar
            dc (int): Cantidad de columnas a trasladar

        Devuelve:
            Coord: Las coordenadas de la celda trasladada
        """

        return Coord(self.fila + df, self.columna + dc)

    def distancia(self, otra):
        """Distancia entre dos celdas.

        Argumentos:
            otra (Coord)

        Devuelve:
            int|float: La distancia entre las dos celdas (no negativo)
        """
        return float((((self.fila - otra.fila))**2 + ((self.columna - otra.columna)**2))**0.5)

    def __eq__(self, otra):
        """Determina si dos coordenadas son iguales"""
        return otra != None and self.fila == otra.fila and self.columna == otra.columna

    def __iter__(self):
        """Iterar las componentes de la coordenada.

        Devuelve un iterador de forma tal que:
        >>> coord = Coord(3, 5)
        >>> f, c = coord
        >>> assert f == 3
        >>> assert c == 5
        """
        for coord in self.fila, self.columna:
            yield coord 

    def __hash__(self):
        """Código "hash" de la instancia inmutable."""
        # Este método es llamado por la función de Python hash(objeto), y debe devolver
        # un número entero.
        # Más información (y un ejemplo de cómo implementar la funcion) en:
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        return hash((self.fila, self.columna))

    def __repr__(self):
        """Representación de la coordenada como cadena de texto"""
        return f"({self.fila},{self.columna})"

    def obtener_celda_intermedia(self, coord):
        """Devuelve la celda intermedia entre self y coord"""
        if self.fila == coord.fila and self.columna == coord.columna -2:
            return Coord(self.fila, self.columna + 1)
        if self.columna == coord.columna and self.fila == coord.fila -2:
            return Coord(self.fila +1, self.columna)    
        if self.fila == coord.fila and self.columna == coord.columna +2:
            return Coord(self.fila, self.columna -1)
        if self.columna == coord.columna and self.fila == coord.fila +2:
            return Coord(self.fila -1, self.columna)  
        return None #La otra forma era lanzar una excepcion pero preferí devolver None.
class Mapa:
    """
    Representa el mapa de un laberinto en una grilla 2D con:

    * un tamaño determinado (filas y columnas)
    * una celda origen
    * una celda destino
    * 0 o más celdas "bloqueadas", que representan las paredes del laberinto

    Las instancias de Mapa son mutables.
    """
    def __init__(self, filas, columnas):
        """Constructor.

        El mapa creado tiene todas las celdas desbloqueadas, el origen en la celda
        de arriba a la izquierda y el destino en el extremo opuesto.

        Argumentos:
            filas, columnas (int): Tamaño del mapa
        """
        self.filas = filas
        self.columnas = columnas
        self.bloqueadas = []
        self.actual = self.origen()
        self.iterando = False
    
    def dimension(self):
        """Dimensiones del mapa (filas y columnas).

        Devuelve:
            (int, int): Cantidad de filas y columnas
        """
        return (self.filas, self.columnas)

    def origen(self):
        """Celda origen.

        Devuelve:
            Coord: Las coordenadas de la celda origen
        """
        return Coord(1, 1)

    def destino(self):
        """Celda destino.

        Devuelve:
            Coord: Las coordenadas de la celda destino
        """
        return Coord(self.filas - 2, self.columnas - 2)

    def asignar_origen(self, coord):
        """Asignar la celda origen.

        Argumentos:
            coord (Coord): Coordenadas de la celda origen
        """
        self.coord_origen = coord

    def asignar_destino(self, coord):
        """Asignar la celda destino.

        Argumentos:
            coord (Coord): Coordenadas de la celda destino
        """
        self.coord_destino = coord

    def celda_bloqueada(self, coord):
        """¿La celda está bloqueada?

        Argumentos:
            coord (Coord): Coordenadas de la celda

        Devuelve:
            bool: True si la celda está bloqueada
        """
        return coord in self.bloqueadas

    def bloquear(self, coord):
        """Bloquear una celda.

        Si la celda estaba previamente bloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a bloquear
        """
        if coord not in self.bloqueadas:
            self.bloqueadas.append(coord)
            
    def desbloquear(self, coord):
        """Desbloquear una celda.

        Si la celda estaba previamente desbloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a desbloquear
        """
        indice = None
        for i in range(len(self.bloqueadas)):
            if coord == self.bloqueadas[i]:
                indice = i

        if indice != None:
            self.bloqueadas.pop(indice)

    def alternar_bloque(self, coord):
        """Alternar entre celda bloqueada y desbloqueada.

        Si la celda estaba previamente desbloqueada, la bloquea, y viceversa.

        Argumentos:
            coord (Coord): Coordenadas de la celda a alternar
        """
        if not coord in self.bloqueadas:
            self.bloquear(coord)
        else:
            self.desbloquear(coord)
    
    def es_coord_valida(self, coord):
        """¿Las coordenadas están dentro del mapa?

        Argumentos:
            coord (Coord): Coordenadas de una celda

        Devuelve:
            bool: True si las coordenadas corresponden a una celda dentro del mapa
        """
        return coord.fila <= self.filas and coord.columna <= self.columnas

    def trasladar_coord(self, coord, df, dc):
        """Trasladar una coordenada, si es posible.

        Argumentos:
            coord: La coordenada de una celda en el mapa
            df, dc: La traslación a realizar

        Devuelve:
            Coord: La coordenada trasladada si queda dentro del mapa. En caso
                   contrario, devuelve la coordenada recibida.
        """
        if self.es_coord_valida(coord):
            return coord.trasladar(df, dc)
        return coord
    def __iter__(self):
        """Iterar por las coordenadas de todas las celdas del mapa.

        Se debe garantizar que la iteración cubre todas las celdas del mapa, en
        cualquier orden.

        Ejemplo:
            >>> mapa = Mapa(10, 10)
            >>> for coord in mapa:
            >>>     print(coord, mapa.celda_bloqueada(coord))
        """
        self.iterador = self
        return self

    def __next__(self):
        """Cambia al siguiente valor de __iter__"""
        coordenada_nueva = None
        if self.iterando and self.actual == self.origen():
            self.iterando = False
            raise StopIteration("No hay mas coordenadas")

        if self.actual.fila == self.filas:
            self.actual = Coord(0, 0)
        
        dato = self.actual
        if self.actual.columna + 1 > self.columnas - 1:
            coordenada_nueva = Coord(self.actual.fila + 1, 0)
        else:
            coordenada_nueva = Coord(self.actual.fila, self.actual.columna + 1)
        self.actual = coordenada_nueva
        self.iterando = True
        return dato        
    
    def obtener_vecinos(self, celda):
        """Devuelve los vecinos de la celda actual"""
        vecinos = []
        if celda.fila != 0:
            vecinos.append(Coord(celda.fila -1, celda.columna))
        if celda.columna != 0:
            vecinos.append(Coord(celda.fila, celda.columna - 1))
        if celda.fila < self.filas - 1:
            vecinos.append(Coord(celda.fila + 1, celda.columna))
        if celda.columna < self.columnas - 1:
            vecinos.append(Coord(celda.fila, celda.columna + 1))    
        
        return vecinos
    
    def obtener_vecinos_pares(self, celda):
        """Devuelve los vecinos de la celda actual"""
        vecinos = []
        if celda.fila >= 2:
            vecinos.append(Coord(celda.fila -2, celda.columna))
        if celda.columna >= 2:
            vecinos.append(Coord(celda.fila, celda.columna - 2))
        if celda.fila < self.filas - 2:
            vecinos.append(Coord(celda.fila + 2, celda.columna))
        if celda.columna < self.columnas - 2:
            vecinos.append(Coord(celda.fila, celda.columna + 2))    
        
        return vecinos      
    
    def bloquear_todo(self):
        """Bloquea todas las celdas"""
        for celda in self:
            self.bloquear(celda)