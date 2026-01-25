from dataclasses import dataclass


@dataclass(frozen=True)
class DistritoElectoralFederal:
    """
    Definición del modelo de Distrito Electoral Federal.
    """

    id: int
    proceso_electoral_id: str
    entidad_id: int
    distrito: int  # distrito: lenguaje ubicuo. El par entidad_id & distrito es único
    nombre_cabecera: str  # Será una instancia de limite_localidad

    def __str__(self):
        return f"{self.entidad_id} {self.distrito:02d}"
