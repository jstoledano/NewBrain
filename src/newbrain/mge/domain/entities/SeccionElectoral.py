from dataclasses import dataclass


@dataclass(frozen=True)
class SeccionElectoral:
    """
    Se define el dominio SeccionElectoral.

    Este es el aggregate root y es la unidad mínima de
    """

    id: int
    proceso_electoral_id: int
    entidad_id: int
    distrito_id: int
    distrito_local: int
    municipio_id: int
    seccion: int  # Lenguaje ubicuo. La combinación entidad & sección es única

    def __str__(self):
        return f"{self.entidad_id:02d} {self.seccion:04d}"
