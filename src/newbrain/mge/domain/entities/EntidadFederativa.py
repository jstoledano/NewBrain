from dataclasses import dataclass


@dataclass(frozen=True)
class EntidadFederativa:
    """
    Define una entidad federativa y sus nombres
    """

    entidad: int
    nombre: str  # VERACRUZ DE IGNACIO DE LA LLAVE
    nombre_corto: str  # VERACRUZ
    nombre_clave: str  # VR
    nombre_abrev: str  # VER

    def __str__(self):
        return f"{self.entidad} {self.nombre.upper()}"
