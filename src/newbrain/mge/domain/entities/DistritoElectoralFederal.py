from dataclasses import dataclass


@dataclass(frozen=True)
class DistritoElectoralFederal:
    """
    Definición del modelo de Distrito Electoral Federal.
    """

    id: int
    proceso_electoral_id: int
    entidad_id: int
    distrito: int  # El par entidad_id&distrito es único
    cabecera: str

    def __str__(self):
        return f"{self.entidad_id} {self.distrito:02d}"
