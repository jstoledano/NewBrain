from dataclasses import dataclass


@dataclass(frozen=True)
class Municipio:
    """
    Se define la clase Municipio.

    La creación de nuevos municipios es infrecuente, su creación
    genera un nuevo MGE para la entidad.
    """

    id: int
    proceso_electoral_id: int
    entidad_id: int
    municipio_id: int
    nombre_municipio: str  # La combinación entidad_id & nombre_municipio es única
    nombre_cabecera: str  # Parece un dato obvio, pero existe

    def __str__(self):
        return f"{self.municipio_id:03d} {self.nombre_municipio.upper()}"
