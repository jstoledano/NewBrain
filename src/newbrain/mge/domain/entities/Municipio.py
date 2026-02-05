from dataclasses import dataclass


@dataclass(frozen=True)
class Municipio:
    """
    Se define la clase Municipio.

    La creación de nuevos municipios es infrecuente, su creación
    genera un nuevo MGE para la entidad.
    """

    id: int
    proceso_electoral_id: str
    entidad_id: int   # 29
    municipio_id: int # 033 (El combo entidad_id & municipio_id es único)
    nombre_municipio: str  # TLAXCALA
    nombre_cabecera: str  # TLAXCALA DE XICOHTENCATL

    def __str__(self):
        return f"{self.municipio_id:03d} {self.nombre_municipio.upper()}"
