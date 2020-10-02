class _Nodo:
    """Representa un nodo con un dato y una referencia
    al sig. nodo"""

    def __init__(self, dato, prox):
        self.dato = dato
        self.prox = prox

    def __repr__(self):
        return f"Nodo({self.dato}, {self.prox})"
class Pila:
    
    def __init__(self):
        self.tope = None
        self.actual = None

    def apilar(self, x):
        n = _Nodo(x, self.tope)
        self.tope = n
        self.actual = n

    def desapilar(self):
        if self.esta_vacia():
            raise PilaVacia()
        dato = self.tope.dato
        self.tope = self.tope.prox
        if self.tope == None or self.tope.prox == None:
            self.actual = None
        else:
            self.actual = self.tope.prox

        return dato

    def ver_tope(self):
        if self.esta_vacia():
            raise PilaVacia()
        return self.tope.dato

    def esta_vacia(self):
        return not self.tope

    def __iter__(self):
        """Iterar los elementos de la pila"""
        self.iterador = self
        return self

    def __next__(self):
        """Cambia al siguiente valor de __iter__"""
        if self.actual == None:
            self.actual = self.tope
            raise StopIteration("No hay mas elementos en la pila")
        
        dato = self.actual
        if self.actual == None or self.actual.prox == None:
            self.actual = None
        else:
            self.actual = self.actual.prox

        return dato    

class PilaVacia(Exception):
    def __init__(self):
        super().__init__("Pila vacia")
