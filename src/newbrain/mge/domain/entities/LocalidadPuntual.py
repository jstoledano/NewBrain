from dataclasses import dataclass


@dataclass(frozen=True)
class LocalidadPuntual:
    """
    Se define la clase LocalidadPuntual

    Una LocalidadPuntual es un punto en la geometría que puede tener
    ciudadanos empadronados, por este motivo, la localidad puntual
    es al mismo tiempo una manzana identificada como 9999 donde se
    referencia a la ciudadanía empadronada.
    """

    id: int
    proceso_electoral_id: str
    entidad_int: int
    municipio_int: int
    localidad_id: int
    nombre_localidad: str

    def __str__(self) -> str:
        return f"{self.localidad_id:04d} {self.nombre_localidad.upper()}"
