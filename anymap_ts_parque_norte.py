# Código en Python básico de AnyMap TS del Parque Norte de Madrid

class ParqueNorte:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion

    def mostrar_info(self):
        print(f"Parque {self.nombre} ubicado en {self.ubicacion}")

parque = ParqueNorte("Parque Norte", "Madrid")
parque.mostrar_info()