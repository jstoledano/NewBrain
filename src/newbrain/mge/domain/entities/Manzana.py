from dataclasses import dataclass


@dataclass(frozen=True)
class Manzana:
    """
    Se define la clase Manzana

    Este es el dominio donde se empadrona a la ciudadanía.
    """

    id: int
    proceso_electoral_id: str
    entidad_id: int
    municipio_id: int
    localidad_id: int  # Lenguaje ubicuo. Se refiere a localidad puntual
    seccion_id: int  # La combinación municipio+localidad+seccion es única para cada entidad
    manzana: int

    def __str__(self):
        return f"{self.seccion_id:04d} {self.localidad_id:04d} {self.manzana:04d}"
