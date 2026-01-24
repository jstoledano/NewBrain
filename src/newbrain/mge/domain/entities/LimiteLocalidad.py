from dataclasses import dataclass


@dataclass(frozen=True)
class LimiteLocalidad:
    """
    Se define el dominio LimiteLocalidad.

    Es un área en la cartografía electoral que define una localidad.
    Pese a que el nombre y el área puede coincidir con otras definiciones
    administrativas y cartográficas, como la de INEGI, su uso se limita a la ubicación
    geolectoral ciudadana.
    """

    id: int
    proceso_electoral_id: str
    entidad_id: int
    municipio_id: int
    localidad_id: int  # localidad_id se reinicia por municipio
    nombre_localidad: str

    def __str__(self) -> str:
        return f"{self.localidad_id:04d} {self.nombre_localidad.upper()}"
