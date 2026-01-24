from dataclasses import dataclass


@dataclass(frozen=True)
class DistritoElectoralFederal:
    """
    Definición del modelo de Distrito Electoral Local.
    """

    id: int
    proceso_electoral_id: int
    entidad_id: int
    distrito_local: int  # El par entidad_id&distrito_local es único
    nombre_cabecera: str  # Es una instancia de limite_localidad

    def __str__(self):
        return f"{self.entidad_id} {self.distrito_local:02d}"
