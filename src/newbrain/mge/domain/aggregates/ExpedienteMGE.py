from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Literal

from ..entities.ProcesoElectoral import ProcesoElectoral
from ..entities.EntidadFederativa import EntidadFederativa
from ..entities.DistritoElectoralFederal import DistritoElectoralFederal
from ..entities.DistritoElectoralLocal import DistritoElectoralLocal
from ..entities.Municipio import Municipio
from ..entities.SeccionElectoral import SeccionElectoral
from ..entities.LimiteLocalidad import LimiteLocalidad
from ..entities.LocalidadPuntual import LocalidadPuntual
from ..entities.Manzana import Manzana


NivelGeoElectoral = Literal["entidad", "distrito", "municipio", "seccion"]


class InconsistenciaExpedienteMGE(Exception):
    """Excepción de dominio para inconsistencias dentro del expediente MGE."""


def _to_str(value: object) -> str:
    """Convierte a str preservando semántica para comparar ids heterogéneos."""
    return str(value)


@dataclass
class ExpedienteMGE:
    """
    Agregado raíz del Marco Geográfico Electoral (MGE).

    Un ExpedienteMGE es un clúster de objetos de dominio asociados
    que se tratan como una unidad conceptual única para efectos de
    interpretación, presentación y uso institucional del MGE.

    Invariantes:
    - Coherencia semántica: todos los objetos pertenecen al mismo proceso electoral y entidad.
    - Nivel geoelectoral único: entidad, distrito, municipio o sección.
    - No mezcla de significados: el contenido corresponde solo al nivel declarado.
    """

    proceso: ProcesoElectoral
    entidad: EntidadFederativa
    nivel: NivelGeoElectoral

    # Colecciones (opcionales según el uso del expediente)
    distritos_federales: List[DistritoElectoralFederal] = field(default_factory=list)
    distritos_locales: List[DistritoElectoralLocal] = field(default_factory=list)
    municipios: List[Municipio] = field(default_factory=list)
    secciones: List[SeccionElectoral] = field(default_factory=list)
    limites_localidad: List[LimiteLocalidad] = field(default_factory=list)
    localidades_puntuales: List[LocalidadPuntual] = field(default_factory=list)
    manzanas: List[Manzana] = field(default_factory=list)

    @property
    def id(self) -> str:
        """Identidad compuesta del expediente basada en proceso, entidad y nivel."""
        return f"{self.proceso.id}:{self.entidad.entidad:02d}:{self.nivel}"

    # Fábrica estática para asegurar validaciones de dominio al construir el agregado
    @staticmethod
    def crear(
        *,
        proceso: ProcesoElectoral,
        entidad: EntidadFederativa,
        nivel: NivelGeoElectoral,
        distritos_federales: Optional[List[DistritoElectoralFederal]] = None,
        distritos_locales: Optional[List[DistritoElectoralLocal]] = None,
        municipios: Optional[List[Municipio]] = None,
        secciones: Optional[List[SeccionElectoral]] = None,
        limites_localidad: Optional[List[LimiteLocalidad]] = None,
        localidades_puntuales: Optional[List[LocalidadPuntual]] = None,
        manzanas: Optional[List[Manzana]] = None,
    ) -> "ExpedienteMGE":
        expediente = ExpedienteMGE(
            proceso=proceso,
            entidad=entidad,
            nivel=nivel,
            distritos_federales=list(distritos_federales or []),
            distritos_locales=list(distritos_locales or []),
            municipios=list(municipios or []),
            secciones=list(secciones or []),
            limites_localidad=list(limites_localidad or []),
            localidades_puntuales=list(localidades_puntuales or []),
            manzanas=list(manzanas or []),
        )
        expediente._validar_coherencia()
        expediente._validar_nivel_geoelectoral()
        return expediente

    def descripcion(self) -> str:
        """Resumen humano-legible del expediente."""
        return (
            f"Expediente MGE [{self.id}] — {self.proceso} / {self.entidad}. "
            f"Nivel: {self.nivel}. "
            f"DF: {len(self.distritos_federales)}, DL: {len(self.distritos_locales)}, "
            f"Mun: {len(self.municipios)}, Sec: {len(self.secciones)}, "
            f"Loc: {len(self.limites_localidad) + len(self.localidades_puntuales)}, "
            f"Manzanas: {len(self.manzanas)}"
        )

    # --- Validaciones internas del agregado ---
    def _validar_coherencia(self) -> None:
        """
        Garantiza que todos los objetos pertenecen al mismo proceso y entidad.

        Nota: Algunas entidades usan tipos distintos para `proceso_electoral_id` (str/int).
        Se normaliza a str para la comparación sin perder semántica de igualdad.
        """
        proc_id = _to_str(self.proceso.id)
        ent_id = self.entidad.entidad

        def check(obj_name: str, obj_list: List[object], get_proc, get_ent) -> None:
            for o in obj_list:
                if _to_str(get_proc(o)) != proc_id:
                    raise InconsistenciaExpedienteMGE(
                        f"{obj_name} con proceso_electoral_id={get_proc(o)} no coincide con {proc_id}"
                    )
                if get_ent(o) != ent_id:
                    raise InconsistenciaExpedienteMGE(
                        f"{obj_name} con entidad_id={get_ent(o)} no coincide con {ent_id}"
                    )

        check(
            "DistritoElectoralFederal",
            self.distritos_federales,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        check(
            "DistritoElectoralLocal",
            self.distritos_locales,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        check(
            "Municipio", self.municipios, lambda x: x.proceso_electoral_id, lambda x: x.entidad_id
        )
        check(
            "SeccionElectoral",
            self.secciones,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        check(
            "LimiteLocalidad",
            self.limites_localidad,
            lambda x: x.proceso_electoral_id,
            lambda x: x.entidad_id,
        )
        # LocalidadPuntual tiene nombres de campos ligeramente distintos (entidad_int, municipio_int)
        for lp in self.localidades_puntuales:
            if _to_str(lp.proceso_electoral_id) != proc_id:
                raise InconsistenciaExpedienteMGE(
                    f"LocalidadPuntual con proceso_electoral_id={lp.proceso_electoral_id} no coincide con {proc_id}"
                )
            if getattr(lp, "entidad_int", None) != ent_id:
                raise InconsistenciaExpedienteMGE(
                    f"LocalidadPuntual con entidad_int={getattr(lp, 'entidad_int', None)} no coincide con {ent_id}"
                )

        check("Manzana", self.manzanas, lambda x: x.proceso_electoral_id, lambda x: x.entidad_id)

    def _validar_nivel_geoelectoral(self) -> None:
        """
        Garantiza que el contenido corresponde al nivel declarado (entidad, distrito, municipio, sección).

        Reglas pragmáticas:
        - entidad: sin restricciones adicionales.
        - distrito: exactamente un tipo de distrito (federal o local), al menos uno y solo uno.
          Si hay secciones, deben referenciar ese distrito según su tipo.
        - municipio: requiere al menos un municipio; secciones/loc/ manzanas deben pertenecer a ese municipio.
          Se prohíbe mezclar con distritos para evitar cambios de nivel implícitos.
        - sección: requiere exactamente una sección; opcionalmente puede incluir municipio/contexto
          pero no distritos. Manzanas y localidades deben pertenecer a la sección/municipio asociado.
        """

        if self.nivel == "entidad":
            return

        if self.nivel == "distrito":
            if self.distritos_federales and self.distritos_locales:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito no admite mezclar distritos federales y locales"
                )
            if not self.distritos_federales and not self.distritos_locales:
                raise InconsistenciaExpedienteMGE(
                    "Nivel distrito requiere al menos un distrito (federal o local)"
                )

            if len(self.distritos_federales) > 1 or len(self.distritos_locales) > 1:
                raise InconsistenciaExpedienteMGE("Nivel distrito se limita a un único distrito")

            distrito_tipo = "federal" if self.distritos_federales else "local"
            distrito_id = (
                self.distritos_federales[0].id
                if distrito_tipo == "federal"
                else self.distritos_locales[0].id
            )

            if distrito_tipo == "federal" and any(
                sec.distrito_electoral_federal_id != distrito_id for sec in self.secciones
            ):
                raise InconsistenciaExpedienteMGE(
                    "Sección fuera del distrito federal declarado en el expediente"
                )
            if distrito_tipo == "local" and any(
                sec.distrito_electoral_local_id != distrito_id for sec in self.secciones
            ):
                raise InconsistenciaExpedienteMGE(
                    "Sección fuera del distrito local declarado en el expediente"
                )
            return

        if self.nivel == "municipio":
            if not self.municipios:
                raise InconsistenciaExpedienteMGE("Nivel municipio requiere al menos un municipio")
            if self.distritos_federales or self.distritos_locales:
                raise InconsistenciaExpedienteMGE("Nivel municipio no debe incluir distritos")

            muni_ids = {m.municipio_id for m in self.municipios}

            if any(sec.municipio_id not in muni_ids for sec in self.secciones):
                raise InconsistenciaExpedienteMGE(
                    "Sección fuera del municipio declarado en el expediente"
                )
            if any(ll.municipio_id not in muni_ids for ll in self.limites_localidad):
                raise InconsistenciaExpedienteMGE(
                    "Localidad fuera del municipio declarado en el expediente"
                )
            if any(lp.municipio_int not in muni_ids for lp in self.localidades_puntuales):
                raise InconsistenciaExpedienteMGE(
                    "Localidad puntual fuera del municipio declarado en el expediente"
                )
            if any(mz.municipio_id not in muni_ids for mz in self.manzanas):
                raise InconsistenciaExpedienteMGE(
                    "Manzana fuera del municipio declarado en el expediente"
                )
            return

        if self.nivel == "seccion":
            if len(self.secciones) != 1:
                raise InconsistenciaExpedienteMGE("Nivel sección requiere exactamente una sección")
            seccion = self.secciones[0]

            if self.distritos_federales or self.distritos_locales:
                raise InconsistenciaExpedienteMGE(
                    "Nivel sección no incluye distritos para evitar mezcla de niveles"
                )

            if self.municipios:
                if (
                    len(self.municipios) != 1
                    or self.municipios[0].municipio_id != seccion.municipio_id
                ):
                    raise InconsistenciaExpedienteMGE(
                        "Municipio proporcionado no coincide con la sección declarada"
                    )

            seccion_ids_permitidos = {seccion.id, seccion.seccion}
            if any(mz.seccion_id not in seccion_ids_permitidos for mz in self.manzanas):
                raise InconsistenciaExpedienteMGE(
                    "Manzana fuera de la sección declarada en el expediente"
                )
