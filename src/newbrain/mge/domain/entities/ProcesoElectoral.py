from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ProcesoElectoral:
    """
    Representa un proceso electoral en donde funciona
    un Marco Geográfico Electoral aprobado para ese
    proceso electoral específico
    """

    id: str
    nombre_corto: str
    nombre_oficial: str
    fecha_inicio: date
    fecha_fin: date

    def contiene_fecha(self, fecha: date) -> bool:
        """Verifica si la fecha dada está dentro del rango del proceso electoral."""
        return self.fecha_inicio <= fecha <= self.fecha_fin

    def __str__(self) -> str:
        periodo = (
            f"({self.fecha_inicio.year})"
            if self.fecha_inicio.year == self.fecha_fin.year
            else f"({self.fecha_inicio.year % 100:02d}-{self.fecha_fin.year % 100:02d})"
        )
        return f"{self.nombre_corto.upper()} {periodo}"
